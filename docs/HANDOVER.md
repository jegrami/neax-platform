# NEAX Handover Snapshot

Date: 2026-04-25
Project root: `neax/`

## Must-Read First
1. `AGENTS.md`
2. `docs/planning/01-problem-framing.md`
3. `docs/planning/02-mvp-prd.md`
4. `docs/planning/03-data-inventory.md`
5. `docs/planning/04-adr-001-core-architecture.md`
6. `docs/planning/05-adr-002-scoring-method.md`
7. `docs/planning/06-adr-003-stack-repo-and-delivery.md`
8. `docs/planning/07-adr-004-data-refresh-and-quality.md`
9. `docs/references/eae-method-summary.md` (then PDF only if needed)

## Current Architecture/Decisions
- Monorepo (single repo), static-first MVP
- LGA-first analysis
- Public read-only MVP
- Python pipeline with `uv`
- Frontend in `apps/web` (lightweight)

## Current Pipeline Scripts
- `data-pipeline/src/prepare_lga_input.py`
  - Alias-based auto column mapping
  - Required semantic columns validation
  - Writes prepared CSV + ingestion report JSON
- `data-pipeline/src/build_first_artifact.py`
  - Reads prepared CSV
  - Loads scoring config JSON
  - Computes `demand_score`
  - Writes parquet artifact with version
- `data-pipeline/src/run_pipeline.py`
  - Orchestrates prepare -> build

## Config/Data Files
- `data-pipeline/config/scoring.v1.json`
- `data-pipeline/config/scoring.ngo.json`
- `data-pipeline/data/lga_input_real.csv`
- `data-pipeline/data/lga_input_prepared.csv`
- `data-pipeline/data/lga_input_report.json`

## Test Status
- Test suite exists under `data-pipeline/tests`
- Last known status: `14 passed`
- If pytest cache warning/error occurs, set pytest config:
  - `[tool.pytest.ini_options]`
  - `cache_dir = ".pytest_cache_local"`

## Environment Notes
- Windows uv global cache permission issue observed
- Workaround used: `UV_CACHE_DIR=.uv-cache`
- Prefer setting permanent user env var for `UV_CACHE_DIR` to avoid retyping

## Typical Commands
From `data-pipeline/`:
- Run tests: `uv run pytest -q`
- Prepare input: `uv run src/prepare_lga_input.py --input lga_input_real.csv --output lga_input_prepared.csv`
- Build artifact: `uv run src/build_first_artifact.py --config scoring.v1.json --input lga_input_prepared.csv`
- One-shot pipeline: `uv run src/run_pipeline.py --raw-input lga_input_real.csv --config scoring.v1.json`

## Next Recommended Development Step
Integrate first real public dataset ingestion (not synthetic CSV):
1. Add source-specific prep script
2. Map to canonical schema
3. Run through existing prepare/build flow
4. Validate output and ranking behavior
