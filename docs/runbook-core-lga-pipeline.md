# Core LGA Pipeline Runbook

Smallest useful runbook for the current NEAX MVP backend flow.

## Purpose

Run the core pipeline from raw public inputs to a scored LGA artifact.

Current stable stages:
1. raw ingest
2. normalize extracted CSV
3. score normalized CSV

## Inputs

Expected under `data-pipeline/data/raw/`:
- boundary file
- population raster
- source manifest JSON

Health facilities may be provided as:
- a local vector file, or
- an ArcGIS `FeatureServer/MapServer` layer URL

## Step 0: Environment

Run from:

`neax/data-pipeline`

Set local uv cache:

```powershell
$env:UV_CACHE_DIR=".uv-cache"
```

Optional check:

```powershell
uv run pytest -q
```

## Step 1: Raw Ingest

Run `src/ingest_public_lga_source.py`.

Responsibility:
- read raw public sources
- extract LGA-level indicators
- write one extracted CSV

Expected output:
- `data-pipeline/data/raw/<extract>.csv`

Success checks:
- file exists
- row count is plausible
- expected columns are present

## Step 2: Normalize Extracted CSV

Run `src/normalize_public_lga_indicator_csv.py`.

Responsibility:
- map source columns into NEAX canonical schema
- validate required semantics
- clean numeric values
- write normalized CSV, metadata JSON, and report JSON

Required:
- extracted CSV
- sources manifest JSON

Expected outputs:
- `data-pipeline/data/lga_input_real.csv`
- `data-pipeline/data/lga_input_real.metadata.json`
- `data-pipeline/data/lga_input_real_ingest_report.json`

Do not continue if:
- required columns are missing
- all rows are dropped
- manifest metadata is incomplete

## Step 3: Score Normalized CSV

Run `src/score_lga_input.py`.

Responsibility:
- read normalized LGA input
- compute current prototype score
- write scored parquet artifact
- write per-run data manifest

Required:
- normalized CSV
- scoring config
- sources manifest JSON

Expected outputs in `data-artifacts/latest/`:
- `lga_priority_input__<version>__<run_stamp>.parquet`
- `data_manifest__<version>__<run_stamp>.json`

## Step 4: Convenience Command

If raw ingest is already done, `src/run_lga_scoring_pipeline.py` can run:
1. normalize
2. score

It does not replace raw ingest.

## Publish Rule

Do not treat a run as publishable if:
- source provenance is unclear
- required outputs are missing
- normalized rows are unexpectedly low
- checksums/manifests are missing
