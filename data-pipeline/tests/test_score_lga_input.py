import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import uuid

import pandas as pd
import pytest

from score_lga_input import (
    build_run_stamp,
    compute_demand_score,
    load_scoring_config,
    minmax_0_100,
    sha256_file,
    write_data_manifest,
    write_artifact,
)


def test_minmax_equal_values_returns_50():
    values = pd.Series([10, 10, 10])
    normalized = minmax_0_100(values)
    assert (normalized == 50.0).all()


def test_load_scoring_config_rejects_invalid_weight_sum():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    cfg_path = data_dir / f"tmp_bad_config_{uuid.uuid4().hex[:8]}.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": "test",
                "demand_weights": {
                    "population_density": 0.9,
                    "health_facilities": 0.3,
                },
            }
        ),
        encoding="utf-8",
    )

    try:
        with pytest.raises(ValueError, match="must sum to 1.0"):
            load_scoring_config(cfg_path)
    finally:
        if cfg_path.exists():
            cfg_path.unlink()


def test_compute_demand_score_uses_passed_weights():
    df = pd.DataFrame(
        {
            "lga_id": ["NG001", "NG002", "NG003"],
            "population_density": [100, 200, 300],
            "health_facilities": [2, 10, 15],
        }
    )

    score_pop_heavy = compute_demand_score(
        df, {"population_density": 0.9, "health_facilities": 0.1}
    )["demand_score"]
    score_health_heavy = compute_demand_score(
        df, {"population_density": 0.1, "health_facilities": 0.9}
    )["demand_score"]

    assert score_pop_heavy.iloc[1] != score_health_heavy.iloc[1]


def test_build_run_stamp_uses_sortable_utc_format():
    run_stamp = build_run_stamp(datetime(2026, 4, 29, 13, 45, 6, tzinfo=timezone.utc))
    assert run_stamp == "20260429T134506Z"


def test_write_artifact_creates_parquet_and_row_count_matches():
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "data-artifacts" / "latest" / f"tmp_test_{uuid.uuid4().hex[:8]}"
    version = "2026.04.test"
    run_stamp = "20260429T134506Z"
    df = pd.DataFrame(
        {
            "lga_id": ["NG001", "NG002"],
            "demand_score": [12.5, 87.5],
            "artifact_version": [version, version],
            "artifact_run_stamp": [run_stamp, run_stamp],
        }
    )

    try:
        out_file = write_artifact(df, out_dir, version, run_stamp)

        assert out_file.exists()
        assert out_file.name == f"lga_priority_input__{version}__{run_stamp}.parquet"
        reloaded = pd.read_parquet(out_file)
        assert len(reloaded) == len(df)
        assert list(reloaded.columns) == list(df.columns)
    finally:
        if out_dir.exists():
            for p in out_dir.glob("*"):
                p.unlink()
            out_dir.rmdir()


def test_write_data_manifest_records_checksums_and_paths():
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "data-artifacts" / "latest" / f"tmp_manifest_{uuid.uuid4().hex[:8]}"
    data_dir = project_root / "data"
    config_dir = project_root / "config"

    out_dir.mkdir(parents=True, exist_ok=True)
    version = "2026.04.test"
    run_stamp = "20260429T134506Z"
    artifact_file = out_dir / f"lga_priority_input__{version}__{run_stamp}.parquet"
    artifact_file.write_bytes(b"artifact")
    config_path = config_dir / f"tmp_cfg_{uuid.uuid4().hex[:8]}.json"
    input_path = data_dir / f"tmp_input_{uuid.uuid4().hex[:8]}.csv"
    sources_manifest_path = data_dir / f"tmp_manifest_{uuid.uuid4().hex[:8]}.json"
    config_path.write_text(
        '{"version":"x","demand_weights":{"population_density":0.7,"health_facilities":0.3}}',
        encoding="utf-8",
    )
    input_path.write_text(
        "lga_id,lga_name,population_density,health_facilities\nNG001,LGA A,100,5\n",
        encoding="utf-8",
    )
    sources_manifest_path.write_text(
        '{"sources":[{"name":"Test","url":"https://example.com","license":"CC BY 4.0","content_date":"2026-04-29"}]}',
        encoding="utf-8",
    )

    try:
        manifest_file = write_data_manifest(
            out_dir=out_dir,
            version=version,
            run_stamp=run_stamp,
            out_file=artifact_file,
            row_count=1,
            config_path=config_path,
            input_path=input_path,
            sources_manifest_path=sources_manifest_path,
        )

        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        assert manifest_file.name == f"data_manifest__{version}__{run_stamp}.json"
        assert manifest["artifact_sha256"] == sha256_file(artifact_file)
        assert manifest["scoring_config_sha256"] == sha256_file(config_path)
        assert manifest["normalized_input_sha256"] == sha256_file(input_path)
        assert manifest["sources_manifest_sha256"] == sha256_file(sources_manifest_path)
        assert manifest["row_count"] == 1
    finally:
        for path in [artifact_file, config_path, input_path, sources_manifest_path]:
            if path.exists():
                path.unlink()
        if out_dir.exists():
            for p in out_dir.glob("*"):
                p.unlink()
            out_dir.rmdir()


def test_main_writes_artifact_and_data_manifest(monkeypatch):
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    config_dir = project_root / "config"
    out_dir = project_root.parent / "data-artifacts" / "latest"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_scoring_input_{suffix}.csv"
    manifest_name = f"tmp_scoring_sources_{suffix}.json"
    config_name = f"tmp_scoring_config_{suffix}.json"

    input_path = data_dir / input_name
    manifest_path = data_dir / manifest_name
    config_path = config_dir / config_name
    run_stamp = "20260430T101010Z"

    pd.DataFrame(
        {
            "lga_id": ["NG001", "NG002"],
            "lga_name": ["LGA A", "LGA B"],
            "population_density": [100, 200],
            "health_facilities": [5, 10],
        }
    ).to_csv(input_path, index=False)
    manifest_path.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": "Test dataset",
                        "url": "https://example.com/data.csv",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-29",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    config_path.write_text(
        json.dumps(
            {
                "version": "2026.04.test",
                "demand_weights": {
                    "population_density": 0.7,
                    "health_facilities": 0.3,
                },
            }
        ),
        encoding="utf-8",
    )

    artifact_path = out_dir / f"lga_priority_input__2026.04.test__{run_stamp}.parquet"
    data_manifest_path = out_dir / f"data_manifest__2026.04.test__{run_stamp}.json"

    try:
        monkeypatch.setattr(
            "score_lga_input.parse_args",
            lambda: argparse.Namespace(
                config=config_name,
                input=input_name,
                sources_manifest=manifest_name,
            ),
        )
        monkeypatch.setattr("score_lga_input.build_run_stamp", lambda now=None: run_stamp)

        import score_lga_input as sli

        sli.main()

        assert artifact_path.exists()
        assert data_manifest_path.exists()

        scored = pd.read_parquet(artifact_path)
        manifest = json.loads(data_manifest_path.read_text(encoding="utf-8"))
        assert "artifact_run_stamp" in scored.columns
        assert scored["artifact_run_stamp"].nunique() == 1
        assert scored["artifact_run_stamp"].iloc[0] == run_stamp
        assert manifest["artifact_run_stamp"] == run_stamp
        assert manifest["artifact_file"].endswith(artifact_path.name)
    finally:
        for path in [input_path, manifest_path, config_path, artifact_path, data_manifest_path]:
            if path.exists():
                path.unlink()
