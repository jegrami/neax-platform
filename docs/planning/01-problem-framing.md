# Problem Framing: Nigeria Energy Access Explorer (NEAX Platform for short)

Date: April 21, 2026
Status: Draft v1

## 1) Problem Statement
Energy access decisions in Nigeria are often made with fragmented datasets (demand, infrastructure, and social services in separate places), which makes it hard to identify and defend high-impact intervention locations quickly.

## 2) Core User and Decision
Primary user: energy planners and NGO analysts.  
Core decision: "Which LGAs should be prioritized next for energy access interventions, and why?"

## 3) Job To Be Done
When planning electrification interventions, users need a transparent, map-based way to combine demand and supply signals so they can rank locations and justify actions with evidence.

## 4) Current Pain
- Data is public but scattered across many portals.
- Data quality/recency is unclear.
- Existing tools are often too broad, too heavy, or not Nigeria-specific enough for practical use.
- Non-technical stakeholders struggle to interpret raw geospatial data.

## 5) Desired Outcome
In less than 10 minutes, a user should be able to:
- select filters/weights,
- view ranked LGAs,
- inspect why each LGA ranks high,
- export/share findings for action.

## 6) Success Metrics (MVP)
- Time-to-first-priority-list < 10 minutes for a first-time user.
- At least 1 clearly explainable score breakdown per LGA.
- At least 3 external planners/NGO users (pilot) complete a ranking workflow without assistance.

## 7) Non-Goals (MVP)
- Full national least-cost optimization modeling.
- Perfect ground-truth electrification estimates.
- Complex multi-role enterprise workflow.

## 8) Assumptions To Validate
- LGA is the right operational unit for MVP (ward is future phase).
- Users value transparency of scoring more than model complexity.
- Public, free datasets are sufficient for a useful first release.
- Public read-only release is acceptable for initial adoption.
