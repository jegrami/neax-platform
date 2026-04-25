import json
from pathlib import Path
import uuid

import pandas as pd
import pytest

from build_first_artifact import (
    compute_demand_score,
    load_scoring_config,
    minmax_0_100,
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

    # Middle row should change when weights change.
    assert score_pop_heavy.iloc[1] != score_health_heavy.iloc[1]


def test_write_artifact_creates_parquet_and_row_count_matches():
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "data-artifacts" / "latest" / f"tmp_test_{uuid.uuid4().hex[:8]}"
    version = "2026.04.test"
    df = pd.DataFrame(
        {
            "lga_id": ["NG001", "NG002"],
            "demand_score": [12.5, 87.5],
            "artifact_version": [version, version],
        }
    )

    try:
        out_file = write_artifact(df, out_dir, version)

        assert out_file.exists()
        reloaded = pd.read_parquet(out_file)
        assert len(reloaded) == len(df)
        assert list(reloaded.columns) == list(df.columns)
    finally:
        if out_dir.exists():
            for p in out_dir.glob("*"):
                p.unlink()
            out_dir.rmdir()
