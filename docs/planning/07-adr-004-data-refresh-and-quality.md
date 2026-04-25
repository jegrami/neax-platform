# ADR-004: Data Refresh Cadence and Quality Checks

Date: April 22, 2026  
Status: Accepted (Draft)  
Decision Owner: Solo developer

## Context
NEAX depends on public datasets with uneven update cycles and quality. We need a lightweight but strict refresh and validation process that a solo developer can sustain.

## Decision
Adopt a tiered refresh model with mandatory quality gates before publishing new artifacts.

## 1) Refresh Cadence (MVP)
### Tier A: Core operational layers
- LGA boundaries
- population
- grid infrastructure proxy
- health facilities

Cadence: monthly check, quarterly publish (unless urgent correction needed).

### Tier B: Context/enrichment layers
- roads/friction
- solar resource
- night lights

Cadence: quarterly check, semi-annual publish.

### Tier C: Experimental layers
- any new pilot dataset not yet trusted

Cadence: ad hoc; never enabled by default in production.

## 2) Artifact Versioning
Each release must produce:
1. `artifact_version` (for example `2026.04.0`)
2. `data_manifest.json` with source URL, source date, retrieval date, license, checksum
3. changelog entry: added/updated/removed indicators and known caveats

No overwrite without retaining previous manifest for rollback.

## 3) Mandatory Quality Gates
A publish is blocked unless all checks pass:
1. Schema checks:
- required columns present
- geometry validity
- unique LGA IDs
2. Coverage checks:
- >= 95% LGA coverage for core indicators
- missingness report generated
3. Value checks:
- numeric range sanity (no impossible values)
- outlier warning report (p1/p99)
4. Join checks:
- no unexpected row multiplication in joins
- deterministic row count after aggregation
5. Reproducibility checks:
- pipeline run logs saved
- manifest checksums match output files

## 4) Publish/Fail Policy
- If Tier A quality gate fails: do not publish, keep previous artifact live.
- If Tier B fails: publish without failed layer and mark as temporarily unavailable.
- If source licensing becomes unclear: disable layer until resolved.

## 5) Data Quality Flags in UI
Each indicator must expose:
1. `last_updated`
2. `coverage_percent`
3. `quality_flag` (`good`, `limited`, `experimental`)
4. `proxy_notice` where relevant

## 6) Operational Budget Rule
Process must run on free/low-cost tooling:
- local or scheduled lightweight runner
- no mandatory paid ETL service for MVP

If refresh workload exceeds solo capacity for two cycles, reduce cadence before adding infrastructure.

## 7) Why
- Protects trust in outputs.
- Avoids silent data regressions.
- Keeps process realistic for solo delivery.

## Follow-up
1. Add `docs/runbook-data-refresh.md` with step-by-step command sequence.
2. Add automated pipeline check script under `data-pipeline/tests`.
