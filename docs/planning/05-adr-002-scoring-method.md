# ADR-002: Scoring Method and Normalization (MVP)

Date: April 22, 2026  
Status: Accepted (Draft)  
Decision Owner: Solo developer

## Context
NEAX needs a transparent ranking method that non-technical stakeholders can understand, while still being practical with free datasets and fast in-browser computation.

## Decision
Use a transparent weighted composite score at LGA level:

`priority_score = demand_score * w_demand + supply_gap_score * w_supply_gap + inclusion_score * w_inclusion`

Where each component is normalized to `[0, 100]`, and final score is also `[0, 100]`.

Default weights (MVP):
- `w_demand = 0.45`
- `w_supply_gap = 0.40`
- `w_inclusion = 0.15`

Users may tune weights in UI, but default profile is the recommended baseline.

## Operational Scoring Workflow (Algorithm)
NEAX determines priority LGAs in five steps:

1. Select indicators for each component (`demand`, `supply gap`, `inclusion`).
2. Clean and transform each indicator:
- handle missing values,
- apply needed transforms (for example log-distance for long-tail metrics),
- winsorize to reduce extreme outlier distortion.
3. Normalize each indicator to a common `0..100` scale so different units are comparable.
4. Compute component scores as weighted averages of normalized indicators.
5. Compute final `priority_score` as weighted sum of component scores.

In compact form:

`priority_score(lga) = w_demand * D(lga) + w_supply_gap * S(lga) + w_inclusion * I(lga)`

Where:
- `D(lga)` is demand component score in `0..100`
- `S(lga)` is supply-gap component score in `0..100`
- `I(lga)` is inclusion component score in `0..100`
- `w_*` weights sum to `1.0`

This is an algorithm because it is a deterministic sequence of data-processing and scoring steps that maps raw indicators to a final ranking.

## Current Prototype Formula (Implemented Now)
The first implementation is intentionally simple for learning and validation:

`demand_score = 0.7 * norm(population_density) + 0.3 * norm(health_facilities)`

Where `norm(x)` is min-max normalization to `0..100`.

This is not the full NEAX scoring model yet; it is a first production-style building block used to validate the scoring pipeline and artifact generation.

## Indicator Groups (MVP)
### Demand Score
- population density / total population proxy
- settlement concentration
- critical services density (health facilities; schools later if quality is good)

### Supply Gap Score
- distance to grid infrastructure (higher distance = higher gap score)
- low proxy electrification signal (for example low night-lights intensity)
- optional resource feasibility bonus (solar suitability) as tie-breaker, not dominant factor

### Inclusion Score
- underserved-rural emphasis proxy (where data is available and reliable)
- optional conflict/vulnerability layers only if quality and licensing are confirmed

## Normalization Rules
1. Use robust min-max normalization with winsorization:
- Clamp raw values to `p5..p95` (5th and 95th percentile) before scaling.
2. Scale to `[0, 100]` with monotonic direction:
- Higher raw value can map to higher score (`+`) or lower score (`-`) depending on metric meaning.
3. For "distance to grid" and similar gap metrics:
- apply log transform before scaling to reduce long-tail distortion.
4. Missing values:
- if an LGA misses an indicator, reweight within that component using available indicators only, and add a "data completeness warning" flag.

## Explainability Requirement
For every LGA output, NEAX must display:
1. Final score
2. Component scores (`demand`, `supply gap`, `inclusion`)
3. Top contributing indicators
4. Data completeness indicator

## Stakeholder Explanation (Plain Language)
If asked how NEAX decides which LGA needs intervention:

"We combine multiple public indicators of need and access constraints.
Each indicator is converted to the same 0-100 scale, then combined using transparent policy weights.
The final score ranks LGAs by priority signal, and the tool shows exactly which factors drove each LGA's score."

## Why
- Transparent and auditable for planners/NGOs.
- Fast enough for browser-side recomputation.
- Tolerates imperfect public datasets while keeping decisions explainable.

## Alternatives Considered
### A) Black-box ML ranking
Pros: potentially better predictive performance.  
Cons: hard to explain and trust for public-interest planning.

### B) Unweighted average
Pros: very simple.  
Cons: ignores policy priorities and weakens practical usefulness.

### C) Full optimization model (least-cost, network planning)
Pros: rich technical depth.  
Cons: too heavy for MVP and solo execution timeline.

## Consequences
### Positive
- Simple governance and communication with non-technical stakeholders.
- Easy to adjust by scenario profiles.
- Strong fit for phased improvement.

### Negative
- Choice of weights remains a normative decision.
- Proxy quality can limit real-world precision.

## Guardrails
1. Every output page must include "Not a definitive ground-truth electrification map" disclaimer.
2. Every indicator must have source/date/license metadata.
3. Any score change due to new data version must be traceable by artifact version.

## Follow-up
1. Add preset profiles in v1.1:
- `Balanced`
- `Public Service First`
- `Market Expansion First`
2. Add uncertainty banding once enough data quality metadata exists.
