# ADR-003: Tech Stack, Repository Structure, Dependencies, and Git Workflow

Date: April 22, 2026  
Status: Accepted (Draft)  
Decision Owner: Solo developer

## Context
NEAX must be lightweight, low-cost, and maintainable by one developer while still being credible for real-world planning use.

## Decision
Adopt a single-repo, static-first architecture with Python ETL and a lightweight JS frontend.

## 1) Tech Stack (MVP)
### Data Pipeline
- Language: Python 3.12+
- Core libs: `geopandas`, `pandas`, `pyogrio`, `shapely`, `rasterio`, `numpy`, `pyarrow`
- Optional: `duckdb` for fast local analytics during ETL

### Frontend
- Runtime: modern browser ES modules
- Map: `MapLibre GL JS`
- UI/state: lightweight vanilla JS (no heavy framework in MVP)
- Charts: `d3` only where necessary

### Data Artifacts
- Primary analytics artifact: `CSV/Parquet` table by `lga_id`
- Geometry artifact: simplified `GeoJSON` for MVP (migrate to `PMTiles` if needed)
- Metadata artifact: dataset catalog JSON (source, date, license, caveats)

## 2) Repository Structure
Use one repository:

```text
neax/
  apps/
    web/                  # frontend app
  data-pipeline/
    src/                  # ETL scripts
    configs/              # dataset configs
    tests/                # data quality checks
  data-artifacts/
    latest/               # generated outputs for deployment
    versions/             # versioned output manifests (no huge binaries in git)
  docs/
    planning/             # problem framing, PRD, ADRs
  .github/
    workflows/            # CI checks
```

Rationale:
- Single repo minimizes coordination and overhead.
- Clean separation of frontend, ETL code, and artifact outputs.
- Easy future split if team grows.

## 3) Dependency Management
### Python
- Use `uv` for environment + lockfile management.
- Keep dependencies minimal and pinned.
- Maintain `requirements.lock` (or `uv.lock`) for reproducibility.

### JavaScript
- Use `npm` with pinned versions.
- Avoid adding new dependencies unless there is clear value.

## 4) Git Workflow
- Branch model: trunk-based
- Default branch: `main`
- Work pattern:
1. short-lived feature branch
2. small focused commits
3. merge quickly into `main`

- Commit convention: Conventional Commits
  - `feat:`
  - `fix:`
  - `docs:`
  - `chore:`

- Release tagging:
  - `v0.x.y` for MVP phase

## 5) CI/CD and Quality Gates
Minimum CI checks:
1. Python lint + unit tests for ETL utilities
2. Data validation tests on sample fixtures
3. Frontend build/lint
4. Broken link check for metadata source URLs (best-effort)

Deployment model:
1. ETL runs locally or scheduled runner
2. artifacts published to static storage/CDN
3. web app deployed as static site

## 6) Hosting and Cost Strategy
Target near-zero cost:
- Frontend: Cloudflare Pages or Netlify free tier
- Artifacts: Cloudflare R2 or equivalent low-cost object storage
- No mandatory API/database in MVP

Escalation trigger to introduce backend API/PostGIS:
- artifact size hurts UX
- query complexity exceeds client-side practicality
- need authenticated workflows or write operations

## 7) Multi-Repo Decision
Not using multi-repo for MVP.

Reason:
- multi-repo increases overhead for solo dev
- single repo is faster for iteration and simpler release management

Revisit multi-repo only when:
- team expands
- independent release cadence becomes necessary
- operational complexity justifies separation

## Consequences
### Positive
- Fast delivery with low ops burden.
- Clear and teachable architecture.
- Easy to maintain solo.

### Negative
- static artifacts may become limiting with scale.
- careful artifact versioning discipline is required.

## Follow-up
1. Add `ADR-004` data refresh and quality policy.
2. Add `ADR-005` ward enablement criteria and fallback behavior.
