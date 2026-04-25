# Data Inventory (MVP) - NEAX

Date: April 21, 2026  
Status: Working draft  
Legend: `Ready` = likely usable now, `Review` = source/license/quality check needed

| Dataset | Role | Candidate Source | Format | Update Cadence | License | Status | Notes |
|---|---|---|---|---|---|---|---|
| Nigeria LGA boundaries | Analysis unit | GRID3 Nigeria geospatial catalog | GPKG/SHP | Periodic | Source-specific | Ready | Canonical unit for MVP scoring |
| Ward boundaries (partial for later) | Optional finer granularity | GRID3 Nigeria | GPKG/SHP | Periodic | Source-specific | Review | Keep out of MVP scoring if incomplete nationwide |
| Population density / gridded population | Demand | WorldPop Nigeria | GeoTIFF | Periodic | CC BY 4.0 (check layer-specific terms) | Ready | Aggregate to LGA for score inputs |
| Settlement extents | Demand proxy | GRID3 settlement extents | GPKG | Periodic | Source-specific | Review | Useful for service reach and concentrated demand |
| Health facilities | Social demand proxy | GRID3 Nigeria health facilities | GPKG/Feature layer | Periodic | Source-specific | Review | Preferred primary source for MVP |
| Health facilities (fallback) | Social demand proxy | NCDC portal (National Health Facility Registry) | CSV | Periodic | Non-commercial notice shown; verify | Review | Use only after explicit license clearance |
| Roads / travel friction | Accessability proxy | GRID3 roads + friction surfaces | Vector/Raster | Periodic | Source-specific | Review | Optional MVP enhancement |
| Transmission/distribution lines | Supply infrastructure proxy | OSM extracts via Geofabrik | PBF/SHP/GPKG | Frequent | ODbL | Ready | Must comply with ODbL attribution/share requirements |
| Power plants/substations | Supply infrastructure proxy | OSM/OpenInfraMap-derived sources | Vector | Frequent | ODbL / source-specific | Review | Confirm consistency and completeness |
| Solar resource (GHI) | Supply resource proxy | NASA POWER or Global Solar Atlas resources | API/GeoTIFF | Regular | Source-specific | Review | Verify preferred source resolution and terms |
| Nighttime lights (VIIRS) | Electricity access proxy | EOG VIIRS annual composites | GeoTIFF | Annual | Public domain/source terms | Ready | Explicitly label as proxy, not direct access metric |

## Data Processing Plan (MVP)
1. Standardize CRS (`EPSG:4326` ingest, projected CRS for distance ops).
2. Create LGA-level feature table with one row per LGA and normalized indicators.
3. Keep `source_name`, `source_url`, `content_date`, `license`, `pipeline_version` fields per indicator.
4. Publish scoring-ready table + geometry for frontend use.

## Data Governance Rules
- No dataset enters production without license and attribution check.
- Every layer must show "last updated" and "known limitation" in UI metadata.
- Proxies must be labeled as proxies in tooltips/docs to avoid false certainty.

## Immediate Validation Tasks
1. Confirm legal reuse terms for NCDC health facility dataset before any use.
2. Choose one canonical boundary source/version for LGA to avoid joins drifting.
3. Decide single GHI source for MVP to reduce pipeline complexity.
