"""Normalize an already-tabular LGA indicator CSV into the NEAX canonical schema.

This script does not read raw geospatial public sources directly.
It expects a CSV that already contains the LGA-level data we need,
such as `lga_id`, `lga_name`, `population_density`, `health_facilities`, grid
distance in km.
"""
import argparse
import hashlib
import json
import re
from datetime import date, datetime, timezone
from difflib import get_close_matches
from pathlib import Path

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
        "lga_code",
        "lgacode",
        "lga_identifier",
        "admin2_pcode",
        "adm2_pcode",
        "id_lga",
    },
    "lga_name": {
        "lga_name",
        "lganame",
        "lga",
        "lga_label",
        "local_government_area",
        "local_government_name",
        "admin2_name",
        "adm2_name",
        "name",
    },
    "population_density": {
        "population_density",
        "pop_density",
        "population_per_km2",
        "population_km2",
        "pop_km2",
        "density",
    },
    "health_facilities": {
        "health_facilities",
        "health_facility_count",
        "health_count",
        "hf_count",
        "facilities_health",
        "health_facilities_count",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest one real public LGA CSV into NEAX canonical input schema."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV path relative to data-pipeline/data (e.g. raw/grid3_worldpop_lga.csv)",
    )
    parser.add_argument(
        "--output",
        default="lga_input_real.csv",
        help="Output CSV path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--report",
        default="lga_input_real_ingest_report.json",
        help="Ingestion report JSON path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--metadata",
        default="lga_input_real.metadata.json",
        help="Metadata JSON path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--sources-manifest",
        required=True,
        help="Required JSON manifest path under data-pipeline/data describing upstream sources",
    )
    parser.add_argument(
        "--proxy-notice",
        default="population_density and health_facilities are planning proxies, not direct electrification truth.",
        help="Proxy warning to surface in metadata/UI",
    )
    return parser.parse_args()


def resolve_under(base_dir: Path, relative_path: str) -> Path:
    base = base_dir.resolve()
    candidate = (base / relative_path).resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError(f"Path escapes data directory: {relative_path}")
    return candidate


def normalize_col_name(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[\s\-\/]+", "_", value)
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def alias_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for canonical, alias_set in ALIASES.items():
        for alias in alias_set:
            lookup[normalize_col_name(alias)] = canonical
    return lookup


def auto_map_columns(raw_columns: list[str]) -> tuple[dict[str, str], list[str]]:
    lookup = alias_lookup()
    mapping: dict[str, str] = {}
    unmapped: list[str] = []

    for raw in raw_columns:
        canonical = lookup.get(normalize_col_name(raw))
        if canonical:
            mapping[raw] = canonical
        else:
            unmapped.append(raw)

    return mapping, unmapped


def suggest_columns(missing: list[str], raw_columns: list[str]) -> dict[str, list[str]]:
    normalized_raw = {normalize_col_name(c): c for c in raw_columns}
    candidates = list(normalized_raw.keys())
    suggestions: dict[str, list[str]] = {}

    for required in missing:
        matches = get_close_matches(required, candidates, n=3, cutoff=0.55)
        suggestions[required] = [normalized_raw[m] for m in matches]

    return suggestions


def collapse_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    deduped = pd.DataFrame(index=df.index)
    seen: set[str] = set()

    for col in df.columns:
        if col in seen:
            continue
        seen.add(col)

        dupes = [c for c in df.columns if c == col]
        if len(dupes) == 1:
            deduped[col] = df[col]
        else:
            deduped[col] = df.loc[:, dupes].replace("", pd.NA).bfill(axis=1).iloc[:, 0]

    return deduped


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def validate_iso_date(value: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"--content-date must be YYYY-MM-DD, got: {value}") from exc


def load_sources_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError(f"Sources manifest must be a JSON object: {path}")

    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError(f"Sources manifest must include a non-empty 'sources' list: {path}")

    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ValueError(f"Source entry {index} must be a JSON object: {path}")
        for field in ("name", "url", "license", "content_date"):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Source entry {index} missing required field '{field}': {path}")
        validate_iso_date(source["content_date"])

    proxy_notice = manifest.get("proxy_notice")
    if proxy_notice is not None and not isinstance(proxy_notice, str):
        raise ValueError(f"'proxy_notice' must be a string when present: {path}")

    return manifest


def resolve_metadata(args: argparse.Namespace, data_dir: Path) -> dict:
    manifest_path = resolve_under(data_dir, args.sources_manifest)
    if not manifest_path.exists():
        raise FileNotFoundError(f"Sources manifest not found: {manifest_path}")

    manifest = load_sources_manifest(manifest_path)
    return {
        "dataset_name": manifest.get("dataset_name", "Multi-source LGA indicator extract"),
        "proxy_notice": manifest.get("proxy_notice", args.proxy_notice),
        "sources": manifest["sources"],
        "sources_manifest_file": str(manifest_path),
    }


def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    metadata_context = resolve_metadata(args, data_dir)

    src = resolve_under(data_dir, args.input)
    out = resolve_under(data_dir, args.output)
    report_file = resolve_under(data_dir, args.report)
    metadata_file = resolve_under(data_dir, args.metadata)

    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src}")

    df = pd.read_csv(src, dtype=str, keep_default_na=False)
    raw_columns = df.columns.tolist()

    mapping, unmapped = auto_map_columns(raw_columns)
    mapped = df.rename(columns=mapping)
    mapped = collapse_duplicate_columns(mapped)

    missing_required = [c for c in REQUIRED_COLUMNS if c not in mapped.columns]
    suggestions = suggest_columns(missing_required, raw_columns) if missing_required else {}

    if missing_required:
        report = {
            "status": "failed",
            "input_file": str(src),
            "row_count_in": int(len(df)),
            "input_columns": raw_columns,
            "auto_mapping": mapping,
            "unmapped_columns": unmapped,
            "missing_required_columns": missing_required,
            "column_suggestions": suggestions,
        }
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise ValueError(
            f"Missing required columns after auto-mapping: {missing_required}. See {report_file}"
        )

    canonical = mapped[REQUIRED_COLUMNS].copy()

    for col in ("lga_id", "lga_name"):
        canonical[col] = canonical[col].astype(str).str.strip()

    pop_raw = canonical["population_density"].astype(str).str.strip()
    hf_raw = canonical["health_facilities"].astype(str).str.strip()

    pop_num = pd.to_numeric(pop_raw, errors="coerce")
    hf_num = pd.to_numeric(hf_raw, errors="coerce")

    pop_non_numeric = int(((pop_raw != "") & pop_num.isna()).sum())
    hf_non_numeric = int(((hf_raw != "") & hf_num.isna()).sum())

    pop_num = pop_num.where(pop_num >= 0)
    hf_num = hf_num.where(hf_num >= 0)

    canonical["population_density"] = pop_num
    canonical["health_facilities"] = hf_num.fillna(0)

    invalid_required = (
        canonical["lga_id"].eq("")
        | canonical["lga_name"].eq("")
        | canonical["population_density"].isna()
    )
    dropped_invalid_rows = int(invalid_required.sum())
    canonical = canonical.loc[~invalid_required].copy()

    if canonical.empty:
        raise ValueError("All rows invalid after validation; no output produced.")

    aggregated = (
        canonical.groupby(["lga_id", "lga_name"], as_index=False)
        .agg(
            population_density=("population_density", "mean"),
            health_facilities=("health_facilities", "sum"),
        )
        .sort_values(["lga_id", "lga_name"], kind="stable")
    )

    aggregated["population_density"] = aggregated["population_density"].round(6)
    aggregated["health_facilities"] = aggregated["health_facilities"].round().astype("int64")

    out.parent.mkdir(parents=True, exist_ok=True)
    aggregated.to_csv(out, index=False)

    metadata = {
        "dataset_name": metadata_context["dataset_name"],
        "sources": metadata_context["sources"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "proxy_notice": metadata_context["proxy_notice"],
        "input_sha256": sha256_file(src),
        "output_file": str(out),
    }
    if "sources_manifest_file" in metadata_context:
        metadata["sources_manifest_file"] = metadata_context["sources_manifest_file"]
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    report = {
        "status": "ok",
        "input_file": str(src),
        "output_file": str(out),
        "row_count_in": int(len(df)),
        "row_count_out": int(len(aggregated)),
        "dropped_invalid_rows": dropped_invalid_rows,
        "population_density_non_numeric_rows": pop_non_numeric,
        "health_facilities_non_numeric_rows": hf_non_numeric,
        "input_columns": raw_columns,
        "auto_mapping": mapping,
        "unmapped_columns": unmapped,
        "missing_required_columns": [],
        "column_suggestions": {},
        "metadata_file": str(metadata_file),
    }
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Wrote canonical CSV: {out} ({len(aggregated)} rows)")
    print(f"Wrote ingestion metadata: {metadata_file}")
    print(f"Wrote ingestion report: {report_file}")


if __name__ == "__main__":
    main()
