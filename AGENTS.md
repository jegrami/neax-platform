
## Mission
NEAX (Nigeria Energy Access Explorer) is a lightweight, open, Nigeria-focused planning tool that helps energy planners and NGOs prioritize where energy access interventions should happen next.

## Project Status
- Phase: MVP build
- Mode: step-by-step implementation
- Principle: smallest useful change, test, confirm, continue

## Scope (MVP)
- Analysis unit: LGA only
- Access mode: public read-only
- Architecture: static-first (Python ETL + static artifacts + lightweight web app)
- Primary users: energy planners and NGOs

## Non-Goals (MVP)
- Ward-level national analytics
- Authentication/roles/permissions
- Heavy backend/API-first architecture
- Paid data dependencies

## Working Directory Rules
- Active project root: `neax/`
- Implement only inside `neax/` unless explicitly instructed
- `eae-tool`, `eae-database`, and `eae-website` are reference-only and should not be modified by default

## Locked Technical Decisions
- Python: `>=3.12` (develop on 3.12 unless explicitly changed)
- Python tooling: `uv`
- Frontend tooling: `npm`
- Repo model: single monorepo
- Planning docs source of truth: `docs/planning/` ADRs and PRD

## Monorepo Structure
- `apps/web` -> frontend
- `data-pipeline` -> ETL and data checks
- `data-artifacts` -> generated output artifacts and manifests
- `docs/planning` -> decisions and product docs

## Data Governance Rules
- Use free/public datasets by default
- Every dataset must include:
  - source URL
  - license
  - content/update date
  - proxy notice where applicable
- Do not publish new artifacts if quality gates fail
- Preserve artifact version history and manifests for rollback

## Workflow Expectations
- Implement in tiny increments
- After each increment:
  1. run the smallest relevant test/check
  2. report result clearly
  3. propose the next smallest step
- Avoid large refactors unless explicitly approved

## Definition of Done (Task-Level)
A task is done only when:
1. code/config change is applied
2. relevant check/test passes (or failure is explained)
3. decision/documentation is updated if behavior changed
4. concise summary is provided

## Git Conventions
- DO NOT commit code to git. I will do it myself


## Safety and Change Control
- Ask before destructive actions
- Ask before adding heavy dependencies
- Ask before changing locked ADR decisions
- Explicitly call out tradeoffs when proposing alternatives

## Communication Preferences
- Be direct and concise
- Explain "why" behind decisions
- Provide commands and steps in execution order
- Prefer practical implementation guidance over theory

## Engineering Rigor
- Do not accept user suggestions blindly; evaluate each suggestion against project goals, EAE-informed architecture, and software best practices.
- Push back clearly and early when a suggestion is unsafe, brittle, scope-expanding, overly complex, or poor practice, and propose a better alternative.
- Default to the simplest design that can work for the current MVP; do not add complexity, infrastructure, abstractions, or process unless they clearly solve a present problem.
- Prefer small, composable scripts and transparent data flows over monolithic or clever designs. Optimize for inspectability, debuggability, and incremental progress.
- Prioritize performance, security, robustness, and maintainability in all decisions.
- Before writing code, verify each construct is necessary; write economically so every line/character has clear purpose and avoid non-essential imports, abstractions, or boilerplate.
- Teach like a senior engineer mentoring a junior: explain critical tradeoffs, architecture choices, and complex logic before implementation.
- For major changes, state assumptions, risks, and expected impact before proceeding.

## Implementation Style
- Favor a Unix-style engineering approach: simple programs, clean interfaces, visible data flow, and composition over monolithic design.
- Keep policy separate from mechanism. For example: source manifests should hold dataset facts and provenance, while scripts should implement reusable mechanics.
- Prefer clarity over cleverness. Code should be easy to inspect, debug, and explain months later.
- Fold knowledge into data where practical. Use config files, manifests, and explicit artifacts instead of hardcoding assumptions into logic.
- Fail early and noisily when invariants are broken, but keep normal successful runs quiet and unsurprising.
- Build inspectable intermediates when they materially help debugging or reuse, but avoid multiplying files or steps without a clear payoff.
- Prototype before polishing. Get the pipeline working end-to-end in the smallest credible form before expanding scope, optimizing, or generalizing.

## Reference Documents
- `docs/references/energy-access-explorer-data-and-methods.pdf`
  - Purpose: source methodology reference from original EAE.
  - Usage rule: read `docs/references/eae-method-summary.md` first; open full PDF only for unresolved method details.
