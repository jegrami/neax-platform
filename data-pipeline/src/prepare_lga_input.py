from pathlib import Path
import argparse
import json
import re
from difflib import get_close_matches
import pandas as pd


REQUIRED_COLUMNS = [
    "lga_id",
    "lga_name",
    "population_density",
    "health_facilities",
]

ALIASES = {
    "lga_id": {
        "lga_id",
        "lgaid",
        "lga_code",
        "lga_identifier",
    },
    "lga_name": {
        "lga_name",
        "lga",
        "lga_label",
        "local_government_area",
        "local_government_name",
        "name",
    },
    "population_density": {
        "population_density",
        "pop_density",
        "pop_den",
        "population_per_km2",
        "population_km2",
    },
    "health_facilities": {
        "health_facilities",
        "health_facility_count",
        "health_count",
        "hf_count",
        "clinics_count",
        "facilities_health",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="lga_input_real.csv",
        help="Raw CSV filename inside data-pipeline/data",
    )
    parser.add_argument(
        "--output",
        default="lga_input_prepared.csv",
        help="Prepared CSV filename inside data-pipeline/data",
    )
    parser.add_argument(
        "--report",
        default="lga_input_report.json",
        help="Ingestion report filename inside data-pipeline/data",
    )
    return parser.parse_args()


def normalize_col_name(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[\s\-\/]+", "_", value)
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def alias_lookup() -> dict[str, str]:
    lookup = {}
    for canonical, alias_set in ALIASES.items():
        for alias in alias_set:
            lookup[normalize_col_name(alias)] = canonical
    return lookup


def auto_map_columns(raw_columns: list[str]) -> tuple[dict[str, str], list[str]]:
    lookup = alias_lookup()
    mapping = {}
    unmapped = []

    for raw in raw_columns:
        normalized = normalize_col_name(raw)
        canonical = lookup.get(normalized)
        if canonical:
            mapping[raw] = canonical
        else:
            unmapped.append(raw)

    return mapping, unmapped


def suggest_columns(missing: list[str], raw_columns: list[str]) -> dict[str, list[str]]:
    normalized_raw = {normalize_col_name(c): c for c in raw_columns}
    suggestions = {}

    for required in missing:
        candidates = list(normalized_raw.keys())
        matches = get_close_matches(required, candidates, n=3, cutoff=0.55)
        suggestions[required] = [normalized_raw[m] for m in matches]

    return suggestions


def collapse_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    deduped = pd.DataFrame(index=df.index)
    seen = set()

    for col in df.columns:
        if col in seen:
            continue
        seen.add(col)

        duplicate_cols = [c for c in df.columns if c == col]
        if len(duplicate_cols) == 1:
            deduped[col] = df[col]
        else:
            deduped[col] = df.loc[:, duplicate_cols].bfill(axis=1).iloc[:, 0]

    return deduped


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"

    args = parse_args()
    src = data_dir / args.input
    out = data_dir / args.output
    report_file = data_dir / args.report

    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src}")

    df = pd.read_csv(src)
    raw_columns = df.columns.tolist()
    mapping, unmapped = auto_map_columns(raw_columns)

    mapped = df.rename(columns=mapping)
    mapped = collapse_duplicate_columns(mapped)

    missing = [c for c in REQUIRED_COLUMNS if c not in mapped.columns]
    suggestions = suggest_columns(missing, raw_columns) if missing else {}

    report = {
        "input_file": str(src),
        "row_count": int(len(df)),
        "input_columns": raw_columns,
        "auto_mapping": mapping,
        "unmapped_columns": unmapped,
        "missing_required_columns": missing,
        "column_suggestions": suggestions,
    }

    with report_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if missing:
        raise ValueError(
            "Missing required columns after auto-mapping: "
            f"{missing}. See report: {report_file}"
        )

    prepared = mapped[REQUIRED_COLUMNS].copy()

    if prepared.empty:
        raise ValueError(f"Prepared dataset is empty: {src}")

    prepared.to_csv(out, index=False)
    print(f"Wrote prepared input: {out} with {len(prepared)} rows")
    print(f"Wrote ingestion report: {report_file}")


if __name__ == "__main__":
    main()
