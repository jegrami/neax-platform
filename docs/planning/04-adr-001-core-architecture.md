# ADR-001: Core Architecture For Nigeria MVP

Date: April 21, 2026  
Status: Accepted (Draft)  
Decision Owner: Solo developer

## Context
We need to ship a useful Nigeria energy-priority tool quickly, with near-zero budget, while keeping data processing transparent and maintainable.

## Decision
Use a lean static-first 3-part architecture:
1. Python ETL pipeline for ingestion/normalization/aggregation to LGA-level analytics table.
2. Versioned static data artifacts (`GeoParquet/GeoJSON/CSV` and optional `PMTiles`) served from low-cost object/static hosting.
3. Lightweight JavaScript frontend (MapLibre-style map + client-side scoring/filtering) in public read-only mode.

## Why
- Python is strong for geospatial preprocessing.
- Static artifacts remove backend ops burden and keep costs near zero.
- LGA-level scoring is small enough for fast client-side compute.
- Public read-only launch reduces authentication and security complexity.
- This structure keeps an upgrade path to PostGIS if scale/complexity grows.

## Alternatives Considered
### A) Postgres + PostGIS + API from day one
Pros: robust query flexibility and governance.  
Cons: more setup/ops cost and slower solo delivery.

### B) Full EAE stack clone immediately
Pros: feature-rich from day one.  
Cons: high complexity for solo MVP and slower time-to-impact.

### C) Static-only with no ETL discipline
Pros: very simple deployment.  
Cons: brittle updates and weak reproducibility.

## Consequences
### Positive
- Faster iteration on scoring and data quality.
- Better reproducibility via versioned build artifacts and metadata.
- Clear path from MVP to robust platform.

### Negative
- Requires disciplined ETL and artifact versioning.
- Less backend flexibility until later API phase.

## Scope Boundaries
- MVP analysis unit: LGA.
- MVP index model: transparent weighted sum with normalization.
- MVP output: ranked LGAs + map + score explanation.
- MVP access mode: public read-only (no accounts).

## Follow-up ADRs Status
Completed:
1. ADR-002: Scoring formula and normalization method.
2. ADR-003: Stack, repository structure, dependency management, artifact format, and hosting topology.

Remaining (only if needed before build milestones):
1. ADR-004: Data refresh cadence and quality checks.
2. ADR-005: Trigger conditions for moving from static artifacts to PostGIS API.
