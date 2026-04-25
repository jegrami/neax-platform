# MVP PRD: Nigeria Energy Access Explorer (NEAX)

Date: April 21, 2026  
Owner: Solo founder/developer  
Status: Draft v1

## 1) Product Goal
Deliver a simple, open, Nigeria-focused tool that ranks priority LGAs for energy access expansion by combining demand and supply proxies.

## 2) Target Users
- Energy planning teams (government/NGO) as primary users
- NGO program teams and technical advisors
- Secondary users: researchers and journalists

## 3) MVP Scope
### In Scope
- Nigeria map + LGA boundary view (single national operational layer for MVP)
- Layer selection for core demand/supply datasets
- Basic filter controls (range sliders / numeric inputs)
- Weighted scoring model
- Ranked LGA output table
- "Why this rank?" factor breakdown per LGA
- Simple export: CSV + shareable analysis state

### Out of Scope
- Ward-level national analytics in MVP
- Custom user-uploaded datasets
- Advanced forecasting and scenario simulation
- Account systems and enterprise auth

## 4) Core User Flow
1. Open app and select index mode (balanced / demand-heavy / supply-heavy).
2. Enable/disable layers and tune ranges/weights.
3. Generate priority map + ranked LGA list.
4. Open one LGA to view score contribution breakdown.
5. Export CSV or copy share link.

## 5) Functional Requirements
- Must load core national layers and render interactive map.
- Must compute composite score per LGA.
- Must support transparent score decomposition.
- Must persist/share current analysis parameters.

## 6) Non-Functional Requirements
- Fast interaction on mid-range laptop (<2 sec for score recompute target).
- Works on mobile and desktop browsers.
- Public read-only mode (no login for MVP).
- Zero-cost or near-zero-cost hosting target.

## 7) Success Criteria (Release Gate)
- End-to-end ranking workflow works without manual backend intervention.
- At least 1 pilot user confirms output usefulness for a real decision/report.
- No paid dataset dependency.

## 8) Risks
- Dataset licensing constraints.
- Dataset staleness and coverage gaps.
- Misinterpretation of proxies as direct electrification truth.

## 9) Product Messaging Rule
All proxy indicators (for example night-time lights, OSM infrastructure completeness, modeled population surfaces) must be explicitly labeled as "proxy" in dataset metadata and explanatory UI text.

## 10) Open Questions
- Should ranking output default to top 20 or full sortable list?
