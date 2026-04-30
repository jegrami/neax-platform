import argparse
import json
from pathlib import Path
import uuid

import pandas as pd
import pytest

import normalize_public_lga_indicator_csv as pli


def test_normalize_col_name():
    assert pli.normalize_col_name(" Population Density / km2 ") == "population_density_km2"


def test_auto_map_columns_aliases():
    raw_columns = ["LGA Code", "Local Government Area", "Pop_Density", "HF_Count"]
    mapping, unmapped = pli.auto_map_columns(raw_columns)

    assert mapping["LGA Code"] == "lga_id"
    assert mapping["Local Government Area"] == "lga_name"
    assert mapping["Pop_Density"] == "population_density"
    assert mapping["HF_Count"] == "health_facilities"
    assert unmapped == []


def test_suggest_columns_returns_close_matches():
    missing = ["population_density"]
    raw_columns = ["population_dens", "lga_name", "health_facilities"]
    suggestions = pli.suggest_columns(missing, raw_columns)

    assert "population_density" in suggestions
    assert "population_dens" in suggestions["population_density"]


def test_collapse_duplicate_columns_prefers_first_non_null():
    df = pd.DataFrame(
        [
            [None, 10, "NG001"],
            [20, 30, "NG002"],
        ],
        columns=["population_density", "population_density", "lga_id"],
    )

    out = pli.collapse_duplicate_columns(df)
    assert list(out.columns).count("population_density") == 1
    assert out.loc[0, "population_density"] == 10
    assert out.loc[1, "population_density"] == 20


def test_load_sources_manifest_rejects_missing_required_fields():
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"
    manifest_path = data_dir / f"tmp_invalid_sources_{uuid.uuid4().hex[:8]}.json"
    manifest_path.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": "Population",
                        "url": "https://example.com/population",
                        "license": "CC BY 4.0",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    try:
        with pytest.raises(ValueError, match="missing required field 'content_date'"):
            pli.load_sources_manifest(manifest_path)
    finally:
        if manifest_path.exists():
            manifest_path.unlink()


def test_resolve_metadata_uses_manifest_proxy_notice_over_cli_override():
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"
    manifest_name = f"tmp_resolve_sources_{uuid.uuid4().hex[:8]}.json"
    manifest_path = data_dir / manifest_name
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_name": "Pilot",
                "proxy_notice": "Manifest notice.",
                "sources": [
                    {
                        "name": "Population",
                        "url": "https://example.com/population",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-29",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        metadata = pli.resolve_metadata(
            argparse.Namespace(
                sources_manifest=manifest_name,
                proxy_notice="CLI notice.",
            ),
            data_dir,
        )

        assert metadata["dataset_name"] == "Pilot"
        assert metadata["proxy_notice"] == "Manifest notice."
        assert metadata["sources_manifest_file"].endswith(manifest_name)
    finally:
        if manifest_path.exists():
            manifest_path.unlink()


def test_main_writes_report_and_prepared_file(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_input_{suffix}.csv"
    output_name = f"tmp_output_{suffix}.csv"
    report_name = f"tmp_report_{suffix}.json"
    metadata_name = f"tmp_metadata_{suffix}.json"
    manifest_name = f"tmp_sources_manifest_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name
    metadata_path = data_dir / metadata_name
    manifest_path = data_dir / manifest_name

    df = pd.DataFrame(
        {
            "lga code": ["NG001", "NG002"],
            "local government area": ["LGA A", "LGA B"],
            "pop_density": [120, 220],
            "hf_count": [5, 9],
            "extra_col": ["x", "y"],
        }
    )
    df.to_csv(input_path, index=False)
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_name": "Test dataset",
                "proxy_notice": "Test proxy notice.",
                "sources": [
                    {
                        "name": "Test dataset",
                        "url": "https://example.com/data.csv",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-29",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
                metadata=metadata_name,
                sources_manifest=manifest_name,
                proxy_notice="Test proxy notice.",
            ),
        )

        pli.main()

        assert output_path.exists()
        assert report_path.exists()

        prepared = pd.read_csv(output_path)
        assert list(prepared.columns) == pli.REQUIRED_COLUMNS
        assert len(prepared) == 2

        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["row_count_in"] == 2
        assert "auto_mapping" in report
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata["dataset_name"] == "Test dataset"
        assert metadata["sources"][0]["license"] == "CC BY 4.0"
    finally:
        for path in [input_path, output_path, report_path, metadata_path, manifest_path]:
            if path.exists():
                path.unlink()


def test_main_accepts_sources_manifest(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_manifest_input_{suffix}.csv"
    output_name = f"tmp_manifest_output_{suffix}.csv"
    report_name = f"tmp_manifest_report_{suffix}.json"
    metadata_name = f"tmp_manifest_metadata_{suffix}.json"
    manifest_name = f"tmp_sources_manifest_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name
    metadata_path = data_dir / metadata_name
    manifest_path = data_dir / manifest_name

    pd.DataFrame(
        {
            "adm2_pcode": ["NG001", "NG002"],
            "adm2_name": ["LGA A", "LGA B"],
            "population_density": [120, 220],
            "health_facility_count": [5, 9],
        }
    ).to_csv(input_path, index=False)

    manifest_path.write_text(
        json.dumps(
            {
                "dataset_name": "GRID3 + WorldPop pilot",
                "proxy_notice": "Proxy test notice.",
                "sources": [
                    {
                        "name": "Boundaries",
                        "url": "https://example.com/boundaries",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-01",
                    },
                    {
                        "name": "Population",
                        "url": "https://example.com/population",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-02",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
                metadata=metadata_name,
                sources_manifest=manifest_name,
                proxy_notice="Ignored because manifest provides one.",
            ),
        )

        pli.main()

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata["dataset_name"] == "GRID3 + WorldPop pilot"
        assert len(metadata["sources"]) == 2
        assert metadata["proxy_notice"] == "Proxy test notice."
        assert metadata["sources_manifest_file"].endswith(manifest_name)
    finally:
        for path in [input_path, output_path, report_path, metadata_path, manifest_path]:
            if path.exists():
                path.unlink()


def test_main_aggregates_duplicate_rows_and_tracks_invalid_values(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_dupes_{suffix}.csv"
    output_name = f"tmp_dupes_out_{suffix}.csv"
    report_name = f"tmp_dupes_report_{suffix}.json"
    metadata_name = f"tmp_dupes_metadata_{suffix}.json"
    manifest_name = f"tmp_dupes_sources_manifest_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name
    metadata_path = data_dir / metadata_name
    manifest_path = data_dir / manifest_name

    pd.DataFrame(
        {
            "adm2_pcode": ["NG001", "NG001", "NG002", ""],
            "adm2_name": ["LGA A", "LGA A", "LGA B", "Bad Row"],
            "population_density": ["100", "200", "oops", "150"],
            "health_facility_count": ["5", "-3", "7", "10"],
        }
    ).to_csv(input_path, index=False)
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_name": "Duplicate test dataset",
                "sources": [
                    {
                        "name": "Test dataset",
                        "url": "https://example.com/data.csv",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-29",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
                metadata=metadata_name,
                sources_manifest=manifest_name,
                proxy_notice="Fallback notice.",
            ),
        )

        pli.main()

        normalized = pd.read_csv(output_path)
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert normalized["lga_id"].tolist() == ["NG001"]
        assert normalized["population_density"].tolist() == [150.0]
        assert normalized["health_facilities"].tolist() == [5]
        assert report["row_count_in"] == 4
        assert report["row_count_out"] == 1
        assert report["dropped_invalid_rows"] == 2
        assert report["population_density_non_numeric_rows"] == 1
    finally:
        for path in [input_path, output_path, report_path, metadata_path, manifest_path]:
            if path.exists():
                path.unlink()


def test_main_raises_if_required_columns_missing_after_mapping(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_missing_{suffix}.csv"
    output_name = f"tmp_missing_out_{suffix}.csv"
    report_name = f"tmp_missing_report_{suffix}.json"
    metadata_name = f"tmp_missing_metadata_{suffix}.json"
    manifest_name = f"tmp_missing_sources_manifest_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name
    metadata_path = data_dir / metadata_name
    manifest_path = data_dir / manifest_name

    pd.DataFrame(
        {
            "lga_name": ["LGA A"],
            "population_density": [100],
        }
    ).to_csv(input_path, index=False)
    manifest_path.write_text(
        json.dumps(
            {
                "dataset_name": "Test dataset",
                "proxy_notice": "Test proxy notice.",
                "sources": [
                    {
                        "name": "Test dataset",
                        "url": "https://example.com/data.csv",
                        "license": "CC BY 4.0",
                        "content_date": "2026-04-29",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
                metadata=metadata_name,
                sources_manifest=manifest_name,
                proxy_notice="Test proxy notice.",
            ),
        )

        with pytest.raises(ValueError, match="Missing required columns after auto-mapping"):
            pli.main()

        assert report_path.exists()
        assert not output_path.exists()
    finally:
        for path in [input_path, output_path, report_path, metadata_path, manifest_path]:
            if path.exists():
                path.unlink()
