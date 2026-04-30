"""Ingest real public geospatial sources into an LGA-level CSV for NEAX.

This is the raw-source ingestion step. It accepts local files or source URLs,
extracts LGA-level indicators from boundaries, rasters, and point layers, and
writes one tabular CSV that the CSV normalizer can validate next.
"""

import argparse
import time
import json
import re
from pathlib import Path
from http.client import IncompleteRead
from urllib.parse import urlencode, urlparse
from urllib.error import URLError
from urllib.request import urlopen, urlretrieve

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping


BOUNDARY_ID_ALIASES = {
    "adm2_pcode",
    "admin2_pcode",
    "lga_id",
    "lga_code",
    "id",
    "lgacode",
}

BOUNDARY_NAME_ALIASES = {
    "adm2_name",
    "admin2_name",
    "lga_name",
    "lga",
    "name",
    "lganame",
}

VECTOR_SUFFIXES = {".gpkg", ".geojson", ".json", ".zip", ".shp"}
RASTER_SUFFIXES = {".tif", ".tiff"}

OUTPUT_COLUMNS = [
    "adm2_pcode",
    "adm2_name",
    "population_density",
    "health_facility_count",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract real LGA-level indicators from raw public geospatial data."
    )
    parser.add_argument(
        "--boundaries",
        required=True,
        help="Boundary source under data/ or a URL",
    )
    parser.add_argument(
        "--population-raster",
        required=True,
        help="Population raster source under data/ or a URL",
    )
    parser.add_argument(
        "--health-facilities",
        required=True,
        help="Health facilities source under data/ or a URL",
    )
    parser.add_argument(
        "--output",
        default="raw/grid3_worldpop_lga_extract.csv",
        help="Output CSV path under data/",
    )
    parser.add_argument(
        "--cache-dir",
        default="raw/_cache",
        help="Cache directory under data/ for downloaded URL sources",
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


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def sanitize_stem(value: str) -> str:
    parsed = urlparse(value)
    raw = parsed.path.rsplit("/", 1)[-1] or parsed.netloc
    stem = Path(raw).stem or "download"
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "_", stem).strip("._-")
    return stem or "download"


def suffix_from_url(url: str, fallback: str) -> str:
    path = urlparse(url).path.lower()
    for suffix in sorted(VECTOR_SUFFIXES | RASTER_SUFFIXES, key=len, reverse=True):
        if path.endswith(suffix):
            return suffix
    return fallback


def arcgis_layer_url(value: str) -> bool:
    return re.search(r"/(FeatureServer|MapServer)/\d+/?$", value, flags=re.IGNORECASE) is not None


def read_json_url(url: str, retries: int = 3, delay_seconds: float = 1.0) -> dict:
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with urlopen(url) as response:
                return json.load(response)
        except (IncompleteRead, URLError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(delay_seconds * attempt)

    raise RuntimeError(f"Failed to read JSON from URL after {retries} attempts: {url}") from last_error


def download_file(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        urlretrieve(url, dest)
    return dest


def export_arcgis_layer_to_geojson(layer_url: str, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_file = cache_dir / f"{sanitize_stem(layer_url)}.geojson"
    if out_file.exists():
        return out_file

    meta = read_json_url(f"{layer_url}?f=json")
    batch_size = int(meta.get("maxRecordCount", 2000))

    count_params = urlencode(
        {
            "where": "1=1",
            "returnCountOnly": "true",
            "f": "json",
        }
    )
    count_json = read_json_url(f"{layer_url}/query?{count_params}")
    total = int(count_json["count"])

    features: list[dict] = []
    offset = 0

    while offset < total:
        query_params = urlencode(
            {
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "true",
                "outSR": "4326",
                "f": "geojson",
                "resultOffset": str(offset),
                "resultRecordCount": str(batch_size),
            }
        )
        page = read_json_url(f"{layer_url}/query?{query_params}")
        page_features = page.get("features", [])
        if not page_features:
            break
        features.extend(page_features)
        offset += len(page_features)

    collection = {
        "type": "FeatureCollection",
        "features": features,
    }
    out_file.write_text(json.dumps(collection), encoding="utf-8")
    return out_file


def materialize_source(value: str, cache_dir: Path, expected_kind: str, data_dir: Path) -> Path:
    if not is_url(value):
        return resolve_under(data_dir, value)

    if expected_kind == "vector" and arcgis_layer_url(value):
        return export_arcgis_layer_to_geojson(value.rstrip("/"), cache_dir)

    if expected_kind == "vector":
        fallback = ".geojson"
    else:
        fallback = ".tif"

    suffix = suffix_from_url(value, fallback)
    out_file = cache_dir / f"{sanitize_stem(value)}{suffix}"
    return download_file(value, out_file)


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

    if boundaries.crs is None:
        raise ValueError("Boundary source has no CRS defined.")

    return boundaries


def load_health_facilities(path: Path, target_crs) -> gpd.GeoDataFrame:
    facilities = gpd.read_file(path)

    if "geometry" not in facilities.columns:
        raise ValueError("Health facilities source has no geometry column.")
    if facilities.crs is None:
        raise ValueError("Health facilities source has no CRS defined.")

    facilities = facilities[facilities.geometry.notna()].copy()
    facilities = facilities.to_crs(target_crs)
    return facilities[["geometry"]].copy()


def count_facilities_within(boundaries: gpd.GeoDataFrame, facilities: gpd.GeoDataFrame) -> pd.Series:
    joined = gpd.sjoin(
        facilities,
        boundaries[["adm2_pcode", "geometry"]],
        how="inner",
        predicate="within",
    )
    counts = joined.groupby("adm2_pcode").size()
    return boundaries["adm2_pcode"].map(counts).fillna(0).astype("int64")


def masked_mean(src: rasterio.io.DatasetReader, geom) -> float:
    cropped, _ = mask(src, [mapping(geom)], crop=True, filled=False)
    band = cropped[0]

    if np.ma.isMaskedArray(band):
        values = band.compressed()
    else:
        values = band.ravel()

    values = values[np.isfinite(values)]
    if values.size == 0:
        return np.nan
    return float(values.mean())


def compute_population_density(boundaries: gpd.GeoDataFrame, raster_path: Path) -> pd.Series:
    with rasterio.open(raster_path) as src:
        boundaries_in_raster_crs = boundaries.to_crs(src.crs)
        means = [masked_mean(src, geom) for geom in boundaries_in_raster_crs.geometry]
    return pd.Series(means, index=boundaries.index, dtype="float64")


def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    cache_dir = resolve_under(data_dir, args.cache_dir)

    boundaries_path = materialize_source(args.boundaries, cache_dir, "vector", data_dir)
    raster_path = materialize_source(args.population_raster, cache_dir, "raster", data_dir)
    facilities_path = materialize_source(args.health_facilities, cache_dir, "vector", data_dir)
    output_path = resolve_under(data_dir, args.output)

    boundaries = load_boundaries(boundaries_path, args.max_lgas)
    facilities = load_health_facilities(facilities_path, boundaries.crs)

    out = boundaries[["adm2_pcode", "adm2_name"]].copy()
    out["health_facility_count"] = count_facilities_within(boundaries, facilities)
    out["population_density"] = compute_population_density(boundaries, raster_path)

    out = out[OUTPUT_COLUMNS].copy()
    out = out.sort_values(["adm2_pcode", "adm2_name"], kind="stable")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Wrote extracted LGA CSV: {output_path}")
    print(f"Boundary source: {boundaries_path}")
    print(f"Population raster source: {raster_path}")
    print(f"Health facilities source: {facilities_path}")
    print(f"Rows: {len(out)}")
    print("Columns:", OUTPUT_COLUMNS)
    print(f"Population density missing rows: {int(out['population_density'].isna().sum())}")


if __name__ == "__main__":
    main()
