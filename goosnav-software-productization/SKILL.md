---
name: goosnav-software-productization
description: Productize local software through gated releases, defaulting to an M1a universal ZIP with stable macOS, Windows, and Linux launcher images that bootstrap dependencies and always open the browser GUI. Use for greenfield apps, standardizing existing apps, local ZIP distribution, launcher design, desktop packaging, CLI/TUI automation, SaaS migration, multi-app operations hubs, digital-download storefronts, or mobile conversion. Keep later gates blocked until the user accepts the working M1a product.
---

# Goosnav Software Productization Protocol

Build one verified milestone at a time. Default to M1a unless the repository records an accepted milestone or the user explicitly requests a later gate. Treat M0 as a brief planning preflight inside M1a, not as a separate user-acceptance blocker.

## Prime directive

Produce the simplest dependable product a customer can launch. Preserve the working application and add only the seams required by the active gate. Plan later stages coarsely; do not scaffold or implement them until the current gate is objectively verified and the user explicitly accepts it.

## Non-negotiable rules

1. Keep one shared domain/application core. Make GUI, CLI, hosted, admin, and mobile surfaces call it through stable contracts.
2. Make the default M1a deliverable one universal ZIP with visible native launcher images for macOS, Windows x64/ARM64, and Linux x86_64/ARM64.
3. Make every M1a launcher resolve the adjacent mutable `app/` directory from its own location. Never embed application code, dependency locks, user data, secrets, or absolute paths in launcher images.
4. Treat a launch that does not display the browser GUI as failure. A launcher may run bootstrap helpers, but it must not substitute a CLI task, batch process, or background-only server.
5. Download a pinned managed Python and exact locked production dependencies automatically. Never require end users to install Python, pip, Node.js, a compiler, or package-manager tooling.
6. Bind local services to `127.0.0.1`, select ports safely, protect state-changing endpoints, and keep secrets/user data outside the repository.
7. Never claim platform or architecture support without building and smoke-testing the corresponding launcher image.
8. Keep failures visible, recoverable, sanitized, and classified with stable diagnostic codes. Exercise the actual launcher and GUI, not unit tests alone.
9. Keep M1a free of DRM, activation, login, copy prevention, and embedded customer credentials. Treat signing, installers, fully offline runtimes, and optional licensing as later work.
10. Stop at `CANDIDATE_FOR_ACCEPTANCE`; only explicit user approval may set `USER_ACCEPTED` or start another milestone.

## Start with repository reconnaissance

Before editing:

1. Inspect the tree, current branch, `git status`, build files, tests, release automation, and existing launch path.
2. Read local agent instructions and private `dev/` documents when present.
3. Identify the canonical command that currently starts the GUI. Preserve it or route it through `app/launcher/bootstrap.py`; do not invent a second business workflow.
4. Determine the lowest defensible current milestone. When no accepted state exists, set M1a active.
5. Record the target user, primary GUI workflow, supported OS/architectures, dependency constraints, data locations, risks, and M1a acceptance procedure.
6. Initialize missing private governance files with `scripts/init_project.py` without overwriting existing content.

Ask only about decisions that materially change product scope, irreversible cost, data handling, licensing, or security. Otherwise make a conservative assumption, record it privately, and continue.

## Milestone states

Use:

`NOT_STARTED -> PLANNED -> ACTIVE -> CANDIDATE_FOR_ACCEPTANCE -> USER_ACCEPTED`

Also allow `BLOCKED` and `DEFERRED`.

- Keep only one milestone `ACTIVE`.
- Let agents move a verified milestone to `CANDIDATE_FOR_ACCEPTANCE`.
- Let only the user move it to `USER_ACCEPTED`.
- Keep future milestones `NOT_STARTED`, `PLANNED`, or `DEFERRED`.
- Keep separate reviewable change sets for separate milestones.

## Default architecture

Use a modular monolith with a simple browser UI and stable application-service boundaries. Default to static HTML/CSS/JavaScript served by the Python backend. Introduce a frontend build system only for demonstrated client-side complexity, and ship its built assets so M1a never installs Node.js on a customer machine.

```text
Native launcher images -> bootstrap/status supervisor -> managed runtime
                                                     -> browser GUI/API
                                                     -> application services
                                                     -> domain core
                                                     -> persistence/provider adapters
```

Keep provider SDKs, persistence, UI frameworks, billing, auth, and platform APIs outside the domain core. Read `references/default-stack.md` for stack choices.

## M1a — Universal ZIP application (default gate)

Make the repository/release root customer-facing:

```text
ProductName-M1a/
├── Open ProductName — macOS.app/
├── Open ProductName — Windows x64.exe
├── Open ProductName — Windows ARM64.exe
├── Open ProductName — Linux x86_64.AppImage
├── Open ProductName — Linux ARM64.AppImage
├── README.txt
├── LICENSE.txt
└── app/
```

Use the reusable source in `assets/m1a-launcher/`. Read `references/zip-app-architecture.md` completely before designing, generating, changing, packaging, or testing M1a launchers.

Require these outcomes:

- Keep the five launcher images stable while `app/src/`, `app/static/`, `app/launcher/manifest.json`, `.python-version`, `pyproject.toml`, and `uv.lock` change.
- Use a small Go supervisor compiled per target. Let it open a loopback setup page immediately, select the bundled `uv`, prepare a versioned runtime, run `app/launcher/bootstrap.py`, wait for readiness, and redirect to the real GUI.
- Bundle one pinned `uv` executable per OS/architecture. Use managed Python, an external application-data environment, `uv sync --locked --no-dev --managed-python --no-build`, and production dependencies with compatible wheels for every claimed target.
- Store runtimes, caches, logs, configuration, database, locks, and runtime state in platform application-data directories, never under the extracted source.
- Reuse a ready runtime when its fingerprint matches. Preserve prior ready environments when an update fails; clean stale partial environments safely.
- Detect an existing healthy instance and reopen it. Supervise new child processes, wait for readiness, expose a GUI quit action, and clean up on failure or termination.
- Show setup progress and actionable browser-based recovery. Map failures to the stable codes defined in the launcher reference and retry only transient network failures.
- Keep `README.txt` limited to choosing the correct launcher, any unavoidable OS trust prompt, data/log locations, and recovery steps.
- Keep application startup independent of private development documents.

M1a fails when any claimed launcher image is missing or untested; setup requires manual developer tooling; dependencies build from source on a customer machine; the launcher depends on its working directory; the server starts without a visible GUI; source-only changes require rebuilding an image; secrets enter the release; or the root confuses the customer.

Set M1a to `CANDIDATE_FOR_ACCEPTANCE` only after the universal ZIP and complete matrix in `references/zip-app-architecture.md` pass. Then stop and present a short acceptance checklist.

## M1b — Signed and packaged edition (optional)

Begin only after M1a is `USER_ACCEPTED` and the user explicitly continues.

Add only the polish the product needs: Developer ID signing/notarization, Windows signing, installers, a fully offline bundled runtime, OS credential storage, automatic updates, or optional licensing/activation. Do not add DRM merely because M1b begins.

M1b passes when clean target systems install or extract the artifact, launch without developer prerequisites, complete the primary workflow, preserve state, update or remove cleanly, and reproduce the build.

## M2 — CLI and optional TUI

Begin only after explicit continuation. Map commands to the same application services as the GUI. Define stable exit codes and `--json`; support noninteractive configuration; test GUI/CLI parity. Build a real event-driven TUI only when it materially improves monitoring or iterative work.

## M3 — Hosted ecosystem

Keep this coarse until activated:

1. Build a repeatable hosted SaaS application foundation with tenant isolation, auth, billing, usage/cost limits, jobs, backups, and observability.
2. Define an authenticated versioned integration contract for app identity, health, subscriptions, entitlements, usage, cost, quota controls, kill switches, and audit events.
3. Build a central owner hub against that contract rather than directly editing every application database.
4. Add a low-cost digital-download storefront whose products, orders, and download entitlements report through the same contract.

Keep provider keys server-side, enforce hard spend caps, verify billing webhooks, and audit privileged actions. Read `references/hosted-saas.md` before planning M3.

## M4 — Mobile

Build mobile clients against the accepted hosted API. Choose Expo/React Native by default for a serious native product; use a web wrapper only for a genuinely web-like experience. Verify current store rules before implementing billing, account deletion, or submission flows.

## Private development and repository hygiene

Store agent instructions, planning, architecture reasoning, software bibles, prompts, and internal release evidence in `dev/` or `dev-private/`. Ignore those directories and top-level `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, and `GEMINI.md` by default.

Commit only material needed to build, run, test, package, operate, or understand the customer-facing product. Ensure ignored documents are never runtime or CI dependencies. If private files were previously tracked, remove them from the index while preserving local copies. Use a private unmerged development branch only when the user explicitly requests it.

Before committing or pushing, inspect `git status` and staged paths. Keep the main branch and release ZIP customer-facing.

## Execution and completion

For each slice:

1. State the active gate and user-visible acceptance criterion.
2. Inspect the existing path before editing.
3. Implement the smallest coherent end-to-end change.
4. Run relevant format, static, unit, integration, launcher, and GUI checks.
5. Record actual evidence and unresolved limitations.
6. Stop when the active gate reaches `CANDIDATE_FOR_ACCEPTANCE`.

Report the active milestone/state, user-visible result, architecture/data changes, exact verification results, unresolved risks, user acceptance steps, and next permitted action.

## Reference loading map

- M1a launcher generation, runtime, errors, packaging, and acceptance: `references/zip-app-architecture.md`
- Stack and dependency choices: `references/default-stack.md`
- Gate definitions: `references/milestones.md`
- Repository and private-document rules: `references/repository-and-docs.md`
- Local security, secrets, and data: `references/security-and-data.md`
- SaaS, hub, storefront, auth, billing, and cost controls: `references/hosted-saas.md`
- Mobile: `references/mobile.md`
- Testing and release evidence: `references/testing-and-release.md`
- Licensing: `references/licensing.md`
- Deviations: `references/decision-rules.md`
- Skill behavior checks: `references/evals.md`

## Explicit user overrides

Follow a direct override unless it creates a security flaw, corrupts data, or makes an acceptance claim false. Record substantial overrides privately. Never use this protocol to ignore a clear product requirement.
