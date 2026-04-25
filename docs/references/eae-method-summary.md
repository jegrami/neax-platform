## Energy Access Explorer: Summary

**What it is:** An open-source, interactive GIS platform developed by WRI to help government planners, off-grid developers, and development finance institutions identify where to expand electricity access in developing countries. It addresses a core gap: existing planning tools optimize for supply costs but largely ignore demand characteristics and affordability.

---

### Data Framework

The platform organizes data into two sides:

**Demand** draws on demographics (population density, poverty rates, household electrification rates) and social/productive use indicators (schools, health facilities, agricultural zones, mines, nighttime lights). Where direct expenditure data is unavailable, proxies like iron sheet roofing, mobile phone ownership, and livestock ownership are used to estimate willingness to pay.

**Supply** covers renewable energy resources (solar irradiance, wind speed, hydro and geothermal potential) and infrastructure proximity (transmission lines, power plants, mini-grids, road accessibility).

Data must meet eight quality criteria: credibility, metadata quality, accuracy, accessibility, spatial coverage, highest available resolution, recency (ideally within five years), and open licensing.

---

### Key Technical Decisions

**Projection:** WGS84 Web Mercator (EPSG:3857) was chosen to enable integration with other online spatial platforms.

**Data processing:** Vector data (points and lines) are converted into distance raster layers, then inverted into proximity rasters normalized 0–1. This lets every square kilometer receive a distinct index value.

**Multi-Criteria Analysis (MCA):** The core analytical engine produces four indices via weighted sums:
- **Demand Index** — weighted normalized demographic + social/productive use data
- **Supply Index** — weighted normalized renewable resources + infrastructure proximity
- **Energy Access Potential** — weighted combination of Demand and Supply indices
- **Need for Assistance Index** — highlights areas with high demand but low ability to pay and poor infrastructure (i.e., where subsidy or development finance is most needed)

All indices are normalized 0–1 using min-max scaling. Weights are user-adjustable, making the analysis customizable per use case.

**Architecture:** PostgreSQL + PostgREST RESTful API, NGINX proxy, JavaScript (ES6) front-end, cloud storage via Amazon S3. Low-resolution datasets are used as filters rather than inputs to the calculation, avoiding the error of applying a single administrative-level value uniformly across large areas.

---

### Notable Design Choices

- The platform is **modular** — new datasets can be added without restructuring the tool
- Local stakeholder engagement (demonstrated in Tanzania) shaped data selection, ensuring country relevance
- Results are downloadable as GIS raster files or PDF reports
- The tool is explicitly positioned as a **complement** to cost-optimization tools (OnSSET, Network Planner), not a replacement — it adds the demand and affordability dimension those tools lack