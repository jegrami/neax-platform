import argparse
import json
from pathlib import Path
import uuid

import pandas as pd
import pytest

import prepare_lga_input as pli


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


def test_main_writes_report_and_prepared_file(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_input_{suffix}.csv"
    output_name = f"tmp_output_{suffix}.csv"
    report_name = f"tmp_report_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name

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

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
            ),
        )

        pli.main()

        assert output_path.exists()
        assert report_path.exists()

        prepared = pd.read_csv(output_path)
        assert list(prepared.columns) == pli.REQUIRED_COLUMNS
        assert len(prepared) == 2

        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["row_count"] == 2
        assert "auto_mapping" in report
    finally:
        for path in [input_path, output_path, report_path]:
            if path.exists():
                path.unlink()


def test_main_raises_if_required_columns_missing_after_mapping(monkeypatch):
    project_root = Path(pli.__file__).resolve().parents[1]
    data_dir = project_root / "data"

    suffix = uuid.uuid4().hex[:8]
    input_name = f"tmp_missing_{suffix}.csv"
    output_name = f"tmp_missing_out_{suffix}.csv"
    report_name = f"tmp_missing_report_{suffix}.json"

    input_path = data_dir / input_name
    output_path = data_dir / output_name
    report_path = data_dir / report_name

    pd.DataFrame(
        {
            "lga_name": ["LGA A"],
            "population_density": [100],
        }
    ).to_csv(input_path, index=False)

    try:
        monkeypatch.setattr(
            pli,
            "parse_args",
            lambda: argparse.Namespace(
                input=input_name,
                output=output_name,
                report=report_name,
            ),
        )

        with pytest.raises(ValueError, match="Missing required columns after auto-mapping"):
            pli.main()

        assert report_path.exists()
        assert not output_path.exists()
    finally:
        for path in [input_path, output_path, report_path]:
            if path.exists():
                path.unlink()
