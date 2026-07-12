---
name: goosnav-software-productization
description: Designs, builds, hardens, and productizes cross-platform software through strict gated milestones: local browser/desktop application, CLI/TUI automation, hosted subscription SaaS, and iOS/Android applications. Use for greenfield app development, standardizing an existing application, architecture and sprint planning, local-first productization, SaaS migration, desktop packaging, automation interfaces, or mobile conversion. Enforces user acceptance gates and prevents premature implementation of later stages.
license: Proprietary. See LICENSE.txt
compatibility: Portable Agent Skill for Claude Code, Codex, and other Agent Skills clients. Requires file and shell access for implementation; Python 3.10+ is required only for the optional project initializer.
metadata:
  author: Goosnav LLC
  version: "1.0.0"
  protocol: GSPP
---

# Goosnav Software Productization Protocol

Apply this protocol to create software that is reliable locally, reusable through automation, commercially operable as SaaS, and distributable on mobile without letting later-stage complexity corrupt the current milestone.

## Prime directive

Build one verified milestone at a time. Plan the complete productization path, but implement only the active milestone. A later milestone may begin only after the current milestone satisfies its exit gate and the user explicitly accepts it.

Universal shippability does **not** mean forcing one executable or one framework onto every platform. It means:

1. one shared domain and application-service core;
2. stable contracts around that core;
3. thin platform-specific adapters for browser, desktop, CLI, TUI, cloud, and mobile;
4. reproducible packaging, tests, documentation, and release evidence for each surface.

## Non-negotiable rules

1. **Never jump milestones.** Future work may be documented, modeled, or represented by interfaces. Do not deploy, scaffold extensively, or implement future-stage features before the active gate passes.
2. **Do not duplicate business logic across interfaces.** GUI, CLI, TUI, hosted API, admin console, and mobile must call the same application services or stable API contracts.
3. **Never make users perform manual environment setup.** The M1a Zip Edition may bootstrap Python, a virtual environment, and locked dependencies through its first-run wizard, but the wizard must be fully automatic, resumable, and produce clear guidance on failure — the user double-clicks and waits. The M1b Packaged Edition and any broadly distributed release must bundle the runtime and dependencies so end users never need Python, Node.js, pip, npm, Docker, or a compiler.
4. **Keep secrets out of the repository, always.** Never commit `.env` or any credential. For the local edition, a GUI-editable, permission-restricted config file (or `.env`) in the platform app-data directory is acceptable for the user's own BYOK keys; the operating-system credential store is the preferred upgrade, required from M1b packaging onward. Hosted secrets belong exclusively in the deployment platform's secret manager.
5. **Keep user data outside the repository.** Use platform application-data directories or a user-selected workspace. Never mix generated projects, logs, databases, caches, uploads, or exports with source code by default.
6. **Bind local services to loopback only.** Default to `127.0.0.1`, not `0.0.0.0`. Use a non-conflicting port and protect local privileged endpoints against cross-origin and cross-site request abuse.
7. **No false cross-platform claims.** “Supports Windows/macOS/Linux” requires actual builds and smoke tests on those operating systems, normally through a CI matrix plus at least one clean-machine manual test per release family.
8. **No false open-source claims.** “All rights reserved” and noncommercial/source-available licenses are not open source. Record the licensing model accurately.
9. **Prefer boring, maintained defaults.** Do not replace the standard stack merely because another tool is fashionable. Deviate only for a documented project constraint and record the decision.
10. **Do not optimize hypothetical scale before product evidence.** Start modular, not distributed. Add services only when workload, security, or operational evidence requires them.
11. **Do not hide failures.** Commands and UI operations must produce actionable errors, structured logs, and stable diagnostic identifiers without leaking secrets.
12. **Do not declare completion from unit tests alone.** Build, launch, and exercise the actual user-facing surface.

## Start every engagement with repository reconnaissance

Before changing code:

1. Inspect the repository tree, git status, current branch, build files, existing instructions, tests, release configuration, and uncommitted work.
2. Determine whether this is a greenfield project, an existing project being standardized, or a migration.
3. Locate and read, in order:
   - `AGENTS.md`
   - `CLAUDE.md` when present
   - `dev/STATE.txt`
   - `dev/NORTHSTAR.txt`
   - `dev/SOFTWARE_BIBLE.txt`
   - `dev/ARCHITECTURE.txt`
   - `dev/TECH_STACK.txt`
   - `dev/ROADMAP.txt`
   - `dev/SPRINT_PLAN.txt`
   - `dev/DECISIONS.txt`
4. If the governance files are absent, initialize them with `scripts/init_project.py` or copy the templates in `assets/project-templates/`. Never overwrite existing files without preserving or merging their content.
5. Identify the current milestone and state. If they are ambiguous, infer the lowest defensible milestone and record the assumption in `dev/DECISIONS.txt`.
6. Summarize the current project contract before implementation:
   - target user and job-to-be-done;
   - active milestone;
   - current acceptance criteria;
   - explicit non-goals;
   - architecture boundaries;
   - primary risks and unknowns.

Ask the user only about decisions that materially alter product scope, irreversible cost, data handling, licensing, or security. Otherwise make a conservative assumption, record it, and continue.

## Milestone state machine

Use these exact states in `dev/STATE.txt`:

`NOT_STARTED -> PLANNED -> ACTIVE -> CANDIDATE_FOR_ACCEPTANCE -> USER_ACCEPTED`

Additional states: `BLOCKED` and `DEFERRED`.

Rules:

- Only one milestone may be `ACTIVE`.
- The agent may move a milestone through `CANDIDATE_FOR_ACCEPTANCE` after objective verification.
- Only explicit user approval may set `USER_ACCEPTED`.
- A future milestone remains `NOT_STARTED` or `PLANNED` until the preceding milestone is `USER_ACCEPTED`.
- A user may explicitly waive a manual gate, but the automated gate and release evidence still must pass. Record the waiver.
- Preserve separate commits or clearly separated change sets for each milestone.

## Plan at two resolutions

Maintain two plans simultaneously:

1. **Productization roadmap:** all milestones, major dependencies, architectural seams, risks, and commercialization path. Keep future milestones coarse.
2. **Active sprint plan:** detailed vertical slices, files likely to change, tests, acceptance procedure, migration/rollback plan, and evidence required for the current milestone only.

Every active plan must contain:

- objective and user-visible outcome;
- in-scope work;
- non-goals;
- assumptions and decisions;
- ordered vertical slices;
- test strategy;
- security/data impact;
- documentation impact;
- rollback or recovery method;
- exit gate.

Do not write a giant speculative implementation plan for all four commercial stages. Detail decays; interfaces and gates endure.

## Default architecture

Use the defaults in `references/default-stack.md` unless a documented constraint requires a deviation. The frontend is simple-first: plain HTML/CSS/JS served by the backend by default, with React/Vite reserved for genuinely complex UIs and recorded as a decision.

The invariant shape is:

```text
Delivery adapters
  Browser UI | Desktop shell | CLI | TUI | Hosted web | Admin | Mobile
                         |
Stable API and application-service contracts
                         |
Domain/application core (business rules, workflows, validation)
                         |
Ports for persistence, files, AI providers, jobs, auth, billing, telemetry
                         |
Adapters selected by milestone (SQLite/local files -> Postgres/object storage/etc.)
```

The application core must not import UI frameworks, Stripe, Supabase, Tauri, React Native, or provider-specific AI SDKs directly. Those are adapters.

## Execution loop for every vertical slice

1. Reconfirm the active milestone and slice acceptance criterion.
2. Inspect existing implementation and tests before editing.
3. Implement the smallest coherent end-to-end slice.
4. Add or update tests at the correct layers.
5. Run formatters, static checks, tests, build, and the actual application surface.
6. Inspect logs and failure behavior.
7. Update affected documentation and decision records.
8. Commit or present a reviewable change set.
9. Continue only when the slice is demonstrably stable.

Do not perform unrelated cleanup, dependency churn, framework replacement, or aesthetic redesign unless it is necessary for the active slice.

## Milestones

### M0 — Product contract and architecture

Purpose: eliminate ambiguity before construction.

Required outputs:

- completed North Star and software bible;
- architecture and data boundaries;
- default stack or approved deviations;
- complete milestone roadmap;
- detailed M1a sprint plan;
- acceptance criteria and test matrix;
- initial threat model and licensing decision;
- repository and branching strategy.

M0 exit gate: the project can be explained as a system, the first sellable local edition is bounded, and no critical decision is being deferred into code by accident.

Read `references/repository-and-docs.md` and `references/decision-rules.md`.

### M1 — Local browser application: Zip Edition, then optional Packaged Edition

Purpose: create a dependable, commercially shippable local product with the fastest possible path to the first sale.

M1 has two sellable sub-editions. M1a is the first revenue gate; M1b is a polish upgrade the user may accept immediately, defer, or skip.

#### M1a — Zip Edition (required, sellable)

Default first-pass architecture: static HTML/CSS/JavaScript served by the Python backend. Do not introduce React, Vite, Node.js, a desktop shell, or another frontend build system unless the escalation conditions in `references/default-stack.md` are met and recorded in `dev/DECISIONS.txt`.

Required outcomes:

* browser-based GUI served by and communicating with a loopback-only backend;
* default simple-first frontend: static HTML/CSS/JS served by the backend;
* stable domain/application core and versioned API contract;
* persistent local projects, settings, database, logs, and exports outside the repository;
* SQLite or equivalent local persistence with migrations, backups, integrity checks, and documented recovery;
* GUI-editable API-key storage in an application-data configuration or secret store, never committed, never returned to the browser after save, and always redacted from logs and support bundles;
* import/export and sanitized support-bundle behavior where applicable;
* launchers `start.command` for macOS, `start.sh` for macOS/Linux, and `start.ps1` for Windows, plus an optional `.bat` compatibility wrapper;
* a top-level double-clickable launcher with a professional icon that routes to the same startup controller;
* a first-run wizard that verifies or obtains a supported Python runtime when permitted, creates the virtual environment, installs exact locked dependencies, initializes or migrates storage, launches the server, and opens the browser without requiring terminal interaction;
* an idempotent startup flow that is safe to rerun after success, partial installation, failed installation, interrupted migration, stale lock files, stale PID files, or a prior crash;
* a resilient localhost startup controller satisfying the Local Server Runtime Contract;
* clean-clone setup for developers;
* a top-level user tutorial, exact API-key acquisition instructions, troubleshooting guide, privacy and data-location guide, and release checklist.

**Local Server Runtime Contract:**

1. Bind only to an explicit loopback address: `127.0.0.1` by default and optionally `::1` when tested. Never bind M1a to `0.0.0.0` by default.
2. Treat the configured port as a preference, not an assumption. Attempt it first. When unavailable, automatically select another free loopback port from a bounded configurable range or use an operating-system-assigned ephemeral port.
3. Resolve port selection and bind the listening socket without a check-then-bind race. Prefer passing a pre-bound socket to the server or retrying atomic bind failures. Never merely probe a port, release it, and assume it remains available.
4. Persist the effective host, port, process ID, start time, application version, and per-launch random session identifier in an application-data runtime-state file using atomic writes. Do not store this state in the repository.
5. Detect a healthy existing instance before starting another. Reuse it and open its URL when versions and workspaces are compatible. Otherwise explain the conflict and provide a safe recovery path. Never terminate an unrelated process merely because it occupies the preferred port.
6. Start the browser only after the health endpoint reports ready and all mandatory migrations and startup checks have passed. Use a bounded timeout, visible progress, and an actionable failure screen or message when readiness is not reached.
7. If startup fails, shut down partially started children, release locks and sockets, preserve diagnostic logs, and return a nonzero exit code. Do not leave zombie processes or report success.
8. Handle `SIGINT`, `SIGTERM`, console-close events, parent-process exit, and normal GUI shutdown. Stop accepting work, allow bounded completion or cancellation, flush logs and database writes, close resources, and terminate children. Force-kill only after the documented grace period expires.
9. Install global exception handlers for the startup controller, HTTP server, background tasks, and worker threads or processes. Convert expected failures into stable user-facing error codes. Log unexpected failures with a correlation ID and sanitized traceback.
10. Provide `/health/live` and `/health/ready`, or equivalent endpoints. Liveness confirms the process loop. Readiness confirms migrations, required storage, configuration, and core dependencies are usable. Neither endpoint may expose secrets.
11. Generate the browser URL from the actual bound address and effective port. Never hardcode `localhost:PORT` in the frontend, launcher, tests, or documentation.
12. Protect local state-changing endpoints with same-origin enforcement and a per-launch unguessable session token or equivalent local authorization mechanism. Restrictive CORS alone is insufficient.
13. Log the preferred port, effective port, fallback reason, startup duration, readiness result, shutdown reason, and crash identifier. Never log API keys, authorization headers, session tokens, or sensitive request bodies.
14. Test at minimum: preferred port free; preferred port occupied by this application; preferred port occupied by an unrelated process; multiple consecutive occupied ports; simultaneous double-launch; stale runtime metadata; interrupted setup; failed migration; browser-open failure; graceful shutdown during active work; forced shutdown after timeout; and restart with preserved state.

M1a exit gate: on a clean supported machine or clean user account, extract the zip, double-click the launcher, watch setup complete unattended, verify automatic port fallback while the preferred port is occupied, complete the primary workflow, restart without losing state, locate logs and user data, export a sanitized support bundle, and recover cleanly from one intentionally induced startup failure. Release evidence must include the actual commands, tests, and resulting logs rather than a prose assertion.


#### M1b — Packaged Edition (recommended upgrade, deferrable)

Required outcomes:

- Tauri desktop shell around the same web UI, with the Python/FastAPI backend bundled as a per-platform sidecar executable;
- self-contained installers/artifacts with professional icons per OS;
- no runtime installation or wizard required for end users;
- secrets migrated to the OS credential store or Tauri secure store.

M1b exit gate: install on clean target systems, launch by double-click, complete the primary workflow, restart without losing state, uninstall or remove cleanly, and reproduce the build from source.

After M1a is `USER_ACCEPTED`, ask the user whether to build M1b now or mark it `DEFERRED` and proceed to M2. Broad public distribution should use M1b.

Read `references/milestones.md`, `references/security-and-data.md`, and `references/testing-and-release.md`.

### M2 — Automation surfaces: CLI, then optional TUI

Purpose: expose proven product capabilities for repeatable automation and community use.

Required outcomes:

- CLI commands map directly to application services, not browser automation;
- complete noninteractive setup and configuration path;
- deterministic exit codes;
- human-readable output by default and stable `--json` output for automation;
- stdin/stdout/file support where appropriate;
- idempotency or explicit overwrite behavior;
- command reference and cheat sheet;
- parity tests between GUI and CLI for shared workflows;
- visually interactive TUI only when it adds material value.

TUI rule: build an event-driven interface with navigation, status, progress, logs, and keyboard help. Do not create numbered prompt menus and call them a TUI.

M2 exit gate: a fresh user can configure and execute the primary workflows without opening the GUI, scripts can depend on documented output contracts, and the TUI—if built—adds value without owning business logic.

Read `references/milestones.md` and `references/testing-and-release.md`.

### M3 — Hosted subscription SaaS and owner command center

Purpose: operate the same product as a secure multi-tenant service with recurring revenue.

Required outcomes:

- hosted web client and Python API/worker deployment;
- tenant-aware Postgres data model, object storage, backups, and migrations;
- Google OAuth plus email OTP/magic-link authentication by default;
- verified-email and abuse controls before costly AI execution;
- server-side provider keys only;
- entitlement, quota, usage-ledger, rate-limit, and hard spend-cap enforcement;
- Stripe products/prices, Checkout, Customer Portal, verified idempotent webhooks, and subscription lifecycle handling;
- three standard tiers plus optional enterprise contact flow;
- background jobs for long or retryable operations;
- transactional email;
- observability, alerting, privacy controls, deletion/export workflows, and incident procedures;
- protected owner command center with role-based access, audit logs, user/subscription/quota/cost/job controls;
- staging environment and a provider setup tutorial.

Free-trial rule: do not rely on IP limits alone. Prefer a useful no-AI demo, BYOK trial, or verified-account quota with CAPTCHA, rate limits, idempotency, anomaly detection, and a hard global budget. A “free model” is not equivalent to zero operational or abuse risk.

M3 exit gate: subscription states correctly grant and revoke entitlements, costs cannot exceed configured limits silently, tenant isolation is tested, backups restore, staging passes end-to-end billing/auth tests, and the owner can operate the service without database surgery.

Read `references/hosted-saas.md`, `references/security-and-data.md`, and `references/testing-and-release.md`.

### M4 — iOS and Android applications

Purpose: deliver a store-compliant mobile product that reuses the hosted service and product contracts.

Required outcomes:

- explicit decision between React Native/Expo and a simpler web wrapper based on required native capability;
- iOS-first design with Android parity plan;
- generated or shared API client and schemas;
- secure session/token storage, deep links, offline/error behavior, and mobile telemetry;
- store-compliant subscription and account-management flow;
- accessibility, privacy manifests/disclosures, screenshots, metadata, support URL, and review notes;
- TestFlight and Android closed-testing evidence;
- crash-free primary workflow on representative devices.

Default: Expo/React Native for a serious product. Use a Capacitor/web wrapper only when the experience is genuinely web-like and store policy risk is acceptable. Do not attempt to ship the local Python sidecar architecture inside the phone app; mobile should normally consume the hosted API.

Before implementing billing or account deletion, verify the current Apple App Store and Google Play rules. Store requirements change and override stale assumptions.

M4 exit gate: signed production builds pass internal review, subscription/account flows comply with current store policy, and the primary paid workflow succeeds on physical iOS and Android devices.

Read `references/mobile.md` and `references/testing-and-release.md`.

## Required repository governance

Every governed project must maintain:

- `AGENTS.md` — agent operating rules and commands;
- `CLAUDE.md` — Claude Code bridge pointing to the shared project rules;
- `dev/STATE.txt` — milestone state and current gate;
- `dev/NORTHSTAR.txt` — intended user experience and core promise;
- `dev/SOFTWARE_BIBLE.txt` — durable product rules, terminology, behavior, and non-goals;
- `dev/ARCHITECTURE.txt` — components, boundaries, data flow, and diagrams;
- `dev/TECH_STACK.txt` — chosen stack, versions/policies, and deviations;
- `dev/ROADMAP.txt` — coarse full productization path;
- `dev/SPRINT_PLAN.txt` — detailed active milestone plan;
- `dev/DECISIONS.txt` — append-only architecture decision log;
- `dev/TEST_PLAN.txt` — test matrix and acceptance procedures;
- `dev/THREAT_MODEL.txt` — assets, trust boundaries, abuse cases, mitigations;
- `dev/RELEASE_CHECKLIST.txt` — release evidence;
- `SETUP.txt` — developer and source-user setup;
- `.env.example` — variable names and safe placeholders only;
- `.gitignore` — secrets, generated data, logs, databases, caches, builds, and user workspaces;
- `LICENSE.txt` — accurate legal distribution model.

Use `.txt` for durable human/product documents as requested. Use Markdown where an AI tool or rendering format benefits materially from it.

## Completion report

At the end of a work cycle, report:

1. active milestone and resulting state;
2. user-visible changes;
3. architecture or data changes;
4. verification commands and results;
5. unresolved risks or blockers;
6. exact user acceptance procedure;
7. next permitted action.

When the active milestone reaches `CANDIDATE_FOR_ACCEPTANCE`, stop implementation of later milestones and give the user a concise acceptance checklist.

## Gotchas

- A `.command`, `.sh`, or `.ps1` launcher plus first-run wizard is a legitimate M1a release format, but it is not a substitute for the M1b packaged edition when distributing broadly or to non-technical buyers.
- An `.ico` file is only an icon asset; Windows applications are `.exe`/`.msi`/MSIX, macOS applications are signed `.app` bundles commonly distributed in `.dmg`/`.pkg`, and Linux releases use formats such as AppImage, `.deb`, or `.rpm`.
- GitHub Pages serves static content and cannot host a Python API, background workers, protected secrets, or subscription webhooks.
- Vercel is suitable for frontend and selected serverless work, but long-running Python/AI jobs need an appropriate API/worker runtime.
- Localhost is still a network boundary. Protect it.
- SQLite-to-Postgres portability is not automatic. Keep persistence behind repositories/ports and test both dialects before SaaS migration.
- Supabase Auth does not replace application authorization, tenant isolation, entitlement checks, or billing state.
- Stripe's client redirect is not proof of payment. Provision from verified webhook state.
- CLI output is an API. Version it and avoid breaking scripts casually.
- Mobile subscription policy is not identical to web billing policy.

## Reference loading map

Load only what the current task requires:

- Stack or architecture choice: `references/default-stack.md`
- Phase scope and gates: `references/milestones.md`
- Repo structure and governance files: `references/repository-and-docs.md`
- Secrets, data, local server, abuse, threat model: `references/security-and-data.md`
- SaaS auth, billing, tiers, jobs, admin: `references/hosted-saas.md`
- Mobile architecture and stores: `references/mobile.md`
- Testing, CI, packaging, release evidence: `references/testing-and-release.md`
- Licensing and public release: `references/licensing.md`
- When to deviate from defaults: `references/decision-rules.md`
- Skill behavior tests: `references/evals.md`

## Explicit user overrides

Follow a direct user override unless it creates a security flaw, corrupts data, or makes the requested acceptance claim false. Record substantial overrides in `dev/DECISIONS.txt`. Never use this protocol as an excuse to ignore a clear product requirement.
