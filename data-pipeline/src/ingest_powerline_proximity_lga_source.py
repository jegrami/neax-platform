"""Extract LGA-level power-line proximity from a raw OSM PBF.

This script reads:
- LGA boundaries
- OSM raw line features from a .osm.pbf

It filters likely power-line features from OSM `other_tags`,
computes the minimum distance from each LGA polygon to the nearest power line,
and writes one LGA-level CSV for downstream normalization/scoring.
"""

import argparse
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd


BOUNDARY_ID_ALIASES = {
    "adm2_pcode",
    "admin2_pcode",
    "lga_id",
    "lga_code",
    "lgacode",
    "id",
}

BOUNDARY_NAME_ALIASES = {
    "adm2_name",
    "admin2_name",
    "lga_name",
    "lga",
    "lganame",
    "name",
}

POWER_TAG_PATTERNS = (
    '"power"=>"line"',
    '"power"=>"minor_line"',
)

OUTPUT_COLUMNS = [
    "adm2_pcode",
    "adm2_name",
    "grid_distance_km",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract LGA-level grid proximity from raw OSM power-line data."
    )
    parser.add_argument(
        "--boundaries",
        required=True,
        help="Boundary source path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--power-lines",
        required=True,
        help="OSM PBF path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--output",
        default="raw/power_line_proximity_lga_extract.csv",
        help="Output CSV path relative to data-pipeline/data",
    )
    parser.add_argument(
        "--max-lgas",
        type=int,
        default=0,
        help="Optional limit for quick pilot runs. 0 means all LGAs.",
    )
    return parser.parse_args()


def normalize(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[\s\-/]+", "_", value)
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def resolve_under(base_dir: Path, relative_path: str) -> Path:
    base = base_dir.resolve()
    candidate = (base / relative_path).resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError(f"Path escapes data directory: {relative_path}")
    return candidate


def find_column(columns: list[str], aliases: set[str], label: str) -> str:
    normalized = {normalize(col): col for col in columns}
    for alias in aliases:
        match = normalized.get(normalize(alias))
        if match:
            return match
    raise ValueError(f"Could not find {label} column. Available columns: {columns}")


def load_boundaries(path: Path, max_lgas: int) -> gpd.GeoDataFrame:
    boundaries = gpd.read_file(path)

    if "geometry" not in boundaries.columns:
        raise ValueError("Boundary source has no geometry column.")
    if boundaries.crs is None:
        raise ValueError("Boundary source has no CRS defined.")

    id_col = find_column(boundaries.columns.tolist(), BOUNDARY_ID_ALIASES, "boundary ID")
    name_col = find_column(boundaries.columns.tolist(), BOUNDARY_NAME_ALIASES, "boundary name")

    boundaries = boundaries[[id_col, name_col, "geometry"]].copy()
    boundaries = boundaries.rename(
        columns={
            id_col: "adm2_pcode",
            name_col: "adm2_name",
        }
    )

    boundaries["adm2_pcode"] = boundaries["adm2_pcode"].astype(str).str.strip()
    boundaries["adm2_name"] = boundaries["adm2_name"].astype(str).str.strip()

    boundaries = boundaries[
        boundaries["adm2_pcode"].ne("")
        & boundaries["adm2_name"].ne("")
        & boundaries.geometry.notna()
    ].copy()

    boundaries = boundaries.sort_values(["adm2_pcode", "adm2_name"], kind="stable")

    if max_lgas > 0:
        boundaries = boundaries.head(max_lgas).copy()

    if boundaries.empty:
        raise ValueError("No usable boundary rows found after filtering.")

    return boundaries


def load_osm_lines(path: Path) -> gpd.GeoDataFrame:
    lines = gpd.read_file(path, layer="lines")

    if "geometry" not in lines.columns:
        raise ValueError("OSM lines layer has no geometry column.")
    if lines.crs is None:
        raise ValueError("OSM lines layer has no CRS defined.")

    return lines[lines.geometry.notna()].copy()


def is_power_line(other_tags: str) -> bool:
    if not isinstance(other_tags, str) or not other_tags:
        return False
    return any(pattern in other_tags for pattern in POWER_TAG_PATTERNS)


def filter_power_lines(lines: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if "other_tags" not in lines.columns:
        raise ValueError("OSM lines layer does not include 'other_tags'.")

    power_lines = lines[lines["other_tags"].apply(is_power_line)].copy()

    if power_lines.empty:
        raise ValueError("No power-line features found after OSM tag filtering.")

    return power_lines[["other_tags", "geometry"]].copy()


def compute_grid_distance_km(
    boundaries: gpd.GeoDataFrame,
    power_lines: gpd.GeoDataFrame,
) -> pd.Series:
    metric_crs = boundaries.estimate_utm_crs()
    if metric_crs is None:
        raise ValueError("Could not estimate a metric CRS for distance calculation.")

    boundaries_m = boundaries.to_crs(metric_crs)
    power_lines_m = power_lines.to_crs(metric_crs)

    distances_m = boundaries_m.geometry.apply(lambda geom: power_lines_m.distance(geom).min())
    return (distances_m / 1000.0).round(6)


def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"

    boundaries_path = resolve_under(data_dir, args.boundaries)
    power_lines_path = resolve_under(data_dir, args.power_lines)
    output_path = resolve_under(data_dir, args.output)

    if not boundaries_path.exists():
        raise FileNotFoundError(f"Boundary file not found: {boundaries_path}")
    if not power_lines_path.exists():
        raise FileNotFoundError(f"Power-lines source not found: {power_lines_path}")

    boundaries = load_boundaries(boundaries_path, args.max_lgas)
    lines = load_osm_lines(power_lines_path)
    power_lines = filter_power_lines(lines)

    out = boundaries[["adm2_pcode", "adm2_name"]].copy()
    out["grid_distance_km"] = compute_grid_distance_km(boundaries, power_lines)

    out = out[OUTPUT_COLUMNS].copy()
    out = out.sort_values(["adm2_pcode", "adm2_name"], kind="stable")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Wrote extracted LGA CSV: {output_path}")
    print(f"Boundary source: {boundaries_path}")
    print(f"Power-lines source: {power_lines_path}")
    print(f"Rows: {len(out)}")
    print("Columns:", OUTPUT_COLUMNS)
    print(f"Power-line features used: {len(power_lines)}")


if __name__ == "__main__":
    main()
