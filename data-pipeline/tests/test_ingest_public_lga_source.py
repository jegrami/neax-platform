import argparse
import json
from http.client import IncompleteRead
from pathlib import Path
import uuid

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

import ingest_public_lga_source as ingest


def test_normalize_strips_symbols_and_spacing():
    assert ingest.normalize(" LGA/Code - 2024 ") == "lga_code_2024"


def test_arcgis_layer_url_detects_supported_service_paths():
    assert ingest.arcgis_layer_url("https://example.com/FeatureServer/0")
    assert ingest.arcgis_layer_url("https://example.com/path/MapServer/12/")
    assert not ingest.arcgis_layer_url("https://example.com/home/item.html?id=abc")


def test_read_json_url_retries_after_incomplete_read(monkeypatch):
    calls = {"count": 0}

    class FakeResponse:
        def __init__(self, payload: str):
            self.payload = payload

        def read(self, *args, **kwargs):
            return self.payload.encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(url):
        calls["count"] += 1
        if calls["count"] == 1:
            raise IncompleteRead(b"partial", 10)
        return FakeResponse('{"ok": true}')

    monkeypatch.setattr(ingest, "urlopen", fake_urlopen)
    monkeypatch.setattr(ingest.time, "sleep", lambda _: None)

    assert ingest.read_json_url("https://example.com/test.json") == {"ok": True}
    assert calls["count"] == 2


def test_export_arcgis_layer_to_geojson_paginates_and_caches(monkeypatch):
    project_root = Path(ingest.__file__).resolve().parents[1]
    cache_dir = project_root / "data" / "raw" / f"_cache_test_{uuid.uuid4().hex[:8]}"
    responses = [
        {"maxRecordCount": 2},
        {"count": 3},
        {
            "features": [
                {"type": "Feature", "properties": {"id": 1}, "geometry": None},
                {"type": "Feature", "properties": {"id": 2}, "geometry": None},
            ]
        },
        {
            "features": [
                {"type": "Feature", "properties": {"id": 3}, "geometry": None},
            ]
        },
    ]
    seen_urls = []

    def fake_read_json_url(url, retries=3, delay_seconds=1.0):
        seen_urls.append(url)
        return responses.pop(0)

    monkeypatch.setattr(ingest, "read_json_url", fake_read_json_url)

    try:
        out_file = ingest.export_arcgis_layer_to_geojson(
            "https://example.com/FeatureServer/0",
            cache_dir,
        )

        payload = json.loads(out_file.read_text(encoding="utf-8"))
        assert out_file.exists()
        assert len(payload["features"]) == 3
        assert any("returnCountOnly=true" in url for url in seen_urls)
        assert sum("/query?" in url for url in seen_urls) == 3

        seen_urls.clear()
        cached_file = ingest.export_arcgis_layer_to_geojson(
            "https://example.com/FeatureServer/0",
            cache_dir,
        )
        assert cached_file == out_file
        assert seen_urls == []
    finally:
        if cache_dir.exists():
            for path in cache_dir.glob("*"):
                path.unlink()
            cache_dir.rmdir()


def test_materialize_source_uses_arcgis_export_for_layer_urls(monkeypatch):
    project_root = Path(ingest.__file__).resolve().parents[1]
    data_dir = project_root / "data"
    cache_dir = data_dir / "raw" / f"_cache_test_{uuid.uuid4().hex[:8]}"
    exported = cache_dir / "cached.geojson"
    cache_dir.mkdir(parents=True, exist_ok=True)
    exported.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")

    try:
        monkeypatch.setattr(ingest, "export_arcgis_layer_to_geojson", lambda url, cache_dir: exported)

        out = ingest.materialize_source(
            "https://example.com/FeatureServer/0",
            cache_dir,
            "vector",
            data_dir,
        )

        assert out == exported
    finally:
        if exported.exists():
            exported.unlink()
        if cache_dir.exists():
            cache_dir.rmdir()


def test_load_boundaries_maps_known_column_aliases_and_applies_limit(monkeypatch):
    gdf = gpd.GeoDataFrame(
        {
            "lgacode": ["1002", "1001", "1003"],
            "lganame": ["B", "A", "C"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
                Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
                Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
            ],
        },
        crs="EPSG:4326",
    )

    monkeypatch.setattr(ingest.gpd, "read_file", lambda path: gdf)

    out = ingest.load_boundaries(Path("dummy.gpkg"), max_lgas=2)

    assert list(out.columns) == ["adm2_pcode", "adm2_name", "geometry"]
    assert out["adm2_pcode"].tolist() == ["1001", "1002"]
    assert out["adm2_name"].tolist() == ["A", "B"]


def test_count_facilities_within_counts_rows_by_lga(monkeypatch):
    boundaries = gpd.GeoDataFrame(
        {
            "adm2_pcode": ["1001", "1002", "1003"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
                Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
                Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
            ],
        },
        crs="EPSG:4326",
    )
    facilities = gpd.GeoDataFrame(
        {"geometry": [Point(0, 0), Point(1, 1), Point(2, 2)]},
        crs="EPSG:4326",
    )
    joined = pd.DataFrame({"adm2_pcode": ["1001", "1001", "1003"]})

    monkeypatch.setattr(ingest.gpd, "sjoin", lambda *args, **kwargs: joined)

    counts = ingest.count_facilities_within(boundaries, facilities)
    assert counts.tolist() == [2, 0, 1]


def test_main_writes_extracted_csv(monkeypatch):
    project_root = Path(ingest.__file__).resolve().parents[1]
    data_dir = project_root / "data"
    suffix = uuid.uuid4().hex[:8]
    output_name = f"raw/tmp_extract_{suffix}.csv"
    output_path = data_dir / output_name

    boundaries = gpd.GeoDataFrame(
        {
            "adm2_pcode": ["1001", "1002"],
            "adm2_name": ["A", "B"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
                Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
            ],
        },
        crs="EPSG:4326",
    )

    try:
        monkeypatch.setattr(
            ingest,
            "parse_args",
            lambda: argparse.Namespace(
                boundaries="raw/boundaries.gpkg",
                population_raster="raw/population.tif",
                health_facilities="https://example.com/FeatureServer/0",
                output=output_name,
                cache_dir="raw/_cache",
                max_lgas=0,
            ),
        )
        monkeypatch.setattr(
            ingest,
            "materialize_source",
            lambda value, cache_dir, expected_kind, data_dir: Path(f"C:/tmp/{expected_kind}.dat"),
        )
        monkeypatch.setattr(ingest, "load_boundaries", lambda path, max_lgas: boundaries.copy())
        monkeypatch.setattr(
            ingest,
            "load_health_facilities",
            lambda path, target_crs: gpd.GeoDataFrame({"geometry": [Point(0.5, 0.5)]}, crs=target_crs),
        )
        monkeypatch.setattr(
            ingest,
            "count_facilities_within",
            lambda boundaries, facilities: pd.Series([3, 7], index=boundaries.index, dtype="int64"),
        )
        monkeypatch.setattr(
            ingest,
            "compute_population_density",
            lambda boundaries, raster_path: pd.Series([12.5, 18.75], index=boundaries.index, dtype="float64"),
        )

        ingest.main()

        out = pd.read_csv(output_path)
        assert list(out.columns) == ingest.OUTPUT_COLUMNS
        assert out["health_facility_count"].tolist() == [3, 7]
        assert out["population_density"].tolist() == [12.5, 18.75]
    finally:
        if output_path.exists():
            output_path.unlink()
