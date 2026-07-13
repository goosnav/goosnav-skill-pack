# Project Agent Instructions

## Governing protocol

This repository follows the Goosnav Software Productization Protocol (GSPP).

Before work, read:

1. `dev/STATE.txt`
2. `dev/NORTHSTAR.txt`
3. `dev/SOFTWARE_BIBLE.txt`
4. `dev/ARCHITECTURE.txt`
5. `dev/TECH_STACK.txt`
6. `dev/SPRINT_PLAN.txt`
7. `dev/DECISIONS.txt`
8. `dev/TEST_PLAN.txt`

## Milestone rule

Implement only the milestone marked ACTIVE in `dev/STATE.txt`. Future milestones may be planned coarsely, but may not be implemented until the active milestone is verified and explicitly accepted by the user.

When no accepted milestone exists, default to M1a. Treat planning as its first slice rather than blocking implementation behind a separate M0 gate. Read the installed skill's `references/zip-app-architecture.md` before launcher work.

## Working rules

- Preserve uncommitted user work.
- Inspect before editing.
- Keep business logic in domain/application services, not UI/CLI/provider adapters.
- Keep user data and secrets outside the repository.
- Never commit `.env`, credentials, local databases, logs, generated workspaces, uploads, caches, or build outputs.
- Add tests with behavior changes.
- Run the actual application surface; tests alone are insufficient.
- Treat a launcher that does not open the browser GUI as failure.
- Keep launcher images independent of mutable `app/` source and dependency manifests.
- Update `dev/STATE.txt`, `dev/SPRINT_PLAN.txt`, `dev/DECISIONS.txt`, and other affected docs.
- Do not add production dependencies without an active requirement and license/security review.
- Do not perform unrelated refactors or framework changes.

## Canonical commands

Replace placeholders as the repository becomes concrete:

- Setup: `TBD`
- Run local: `TBD`
- Format: `TBD`
- Lint: `TBD`
- Type check: `TBD`
- Unit tests: `TBD`
- Integration tests: `TBD`
- End-to-end tests: `TBD`
- Build: `TBD`
- Package: `TBD`
- Smoke test: `TBD`

## Completion report

State the active milestone, changes, verification results, remaining risk, exact user acceptance steps, and the next permitted action.
