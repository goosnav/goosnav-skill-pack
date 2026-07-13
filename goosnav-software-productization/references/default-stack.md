# Default technical architecture

Use this stack as the default, not as dogma. Record every material deviation in `dev/DECISIONS.txt` with its constraint, cost, and migration impact.

## Architectural principle

Use a modular monolith with ports and adapters until measured evidence requires distribution.

```text
Browser web UI ------\
Tauri desktop -------\
Typer CLI ------------> Application services -> Domain rules
Textual TUI ----------/          |                    |
Hosted API -----------/          |                    |
Mobile client --------/      Ports/interfaces         |
                                  |                    |
                     SQLite/Postgres, files/storage, AI providers,
                     jobs, auth, billing, telemetry adapters
```

The domain and application-service layers own:

- validation and business invariants;
- workflows/use cases;
- project/profile semantics;
- provider-independent request/response objects;
- authorization decisions expressed as policies;
- deterministic calculations and transformations.

Adapters own:

- HTTP, web UI, desktop, CLI, TUI, and mobile rendering;
- persistence implementation;
- AI/provider SDKs;
- auth identity parsing;
- billing gateway calls;
- file-system paths;
- telemetry transport;
- job transport.

## Repository tooling

- Git and GitHub.
- Python workspace and lockfile: `uv` by default.
- Stable launcher supervisor: Go standard library, compiled once per supported target from `assets/m1a-launcher/`.
- JavaScript workspace and lockfile: `pnpm` by default.
- Task entry points: a root `Makefile`, `justfile`, or cross-platform scripts. Do not make end-user operation depend on Make.
- Pre-commit checks are encouraged, but CI remains authoritative.

Pin direct dependencies. Commit lockfiles. Automate dependency updates conservatively.

## Python core and API

- Python 3.12+ baseline unless a required binary constrains it.
- FastAPI for the local/hosted HTTP API.
- Pydantic for request, response, settings, and internal boundary models.
- SQLAlchemy 2.x plus Alembic for persistence and migrations.
- SQLite in local edition; Postgres in hosted edition.
- Provider-neutral repository interfaces. Test both dialects before M3 acceptance.
- `httpx` for outbound HTTP.
- `structlog` or standard-library structured logging with JSON output and redaction.
- Local secrets: a permission-restricted config file in the app-data directory for the Zip Edition; `keyring` or a Tauri secure-store/keychain adapter preferred, required from M1b onward.
- `pytest`, Ruff, and a static type checker.

Use C++/Rust acceleration only behind a stable native boundary when profiling proves Python is materially inadequate. Provide deterministic tests comparing accelerated and reference implementations.

## Web UI — simple-first

Default tier (most projects):

- plain HTML, CSS, and JavaScript served as static files by the FastAPI backend — no Node.js, no bundler, no build step;
- optionally htmx and/or Alpine.js as vendored local files for interactivity; never a runtime CDN dependency;
- one coherent hand-owned stylesheet or a small vendored CSS framework;
- fetch calls against the same documented API the CLI and future surfaces use;
- Playwright (driven from the Python test suite) for real browser workflow tests.

Escalation tier — only when the UI has genuinely complex client state (multi-view editors, live dashboards, heavy drag-and-drop, collaborative views), and recorded as a decision in `dev/DECISIONS.txt`:

- React + TypeScript + Vite.
- Tailwind CSS plus shadcn/ui-style source components for a coherent, owned design system.
- TanStack Query for remote/server state; React local state/context first.
- Zod or generated schemas at external boundaries.
- OpenAPI-generated TypeScript API client. Do not hand-maintain duplicate request/response types.
- Vitest for component/unit tests and Playwright for real browser workflows.

Do not escalate for aesthetics alone — the simple tier can look professional. Because all surfaces call the same API contract, upgrading a simple frontend to React later is an adapter swap, not a rewrite.

For a public marketing site requiring server-rendered SEO, add a separate Next.js site in M3. Do not force the product client into a server-rendered architecture merely for a landing page.

## Local packaging

### M1a universal ZIP (default release)

Use the exact root and supervisor protocol in `zip-app-architecture.md`. Ship macOS universal, Windows x64/ARM64, and Linux x86_64/ARM64 launcher images together with one adjacent mutable `app/` payload.

- Compile the same standard-library Go supervisor for every target.
- Bundle pinned `uv` executables under `app/launcher/tools/`.
- Pin an exact managed Python and commit `uv.lock`.
- Set `tool.uv.required-environments` for all six OS/architecture combinations and disable source builds during customer setup.
- Store Python, environments, cache, logs, configuration, database, and runtime state in platform application-data directories.
- Put `app/src` on the bootstrap import path (or use a no-build editable install) so source/static changes take effect without rebuilding launcher images or resynchronizing dependencies.
- Open a loopback status page before downloads and redirect it to the GUI only after readiness.
- Prebuild any frontend assets; never install Node.js or run a customer-machine frontend build.

### M1b signed/offline edition (optional polish)

Add only requested improvements: signing/notarization, installers, a fully offline bundled runtime, OS credential storage, automatic updates, or optional licensing. A Tauri shell plus packaged Python sidecar remains an allowed choice when a native window materially improves the product; it is no longer mandatory merely to pass M1b.

## Local persistence and user workspaces

Default paths are platform application-data directories, resolved by a platform library. Separate:

- configuration;
- secrets;
- database;
- cache;
- logs;
- user-created project workspaces;
- exports.

Each user project should be a self-contained directory with a versioned manifest and user-generated files. Never assume those files are safe to commit.

## CLI and TUI

- Typer for CLI command structure.
- Rich for readable terminal output.
- Textual for a real TUI when justified.
- Same application-service layer as GUI.
- Stable JSON schema under `--json` and documented exit codes.

## Hosted SaaS

Default deployment topology:

- product web client: Vercel static/frontend deployment;
- API and worker containers: Railway by default;
- Postgres, Auth, and object storage: Supabase;
- billing: Stripe Billing/Checkout/Customer Portal;
- transactional email: Resend, connected to Supabase custom SMTP when appropriate;
- jobs: Dramatiq with Redis for long or retryable work;
- error monitoring: Sentry;
- structured logs and metrics: provider logs plus OpenTelemetry-compatible instrumentation.

Provider selection must be rechecked before M3 implementation because capabilities and pricing change. Preserve container portability and standard Postgres so migration remains possible.

## Mobile

Default:

- Expo + React Native + TypeScript;
- Expo Router;
- EAS Build/Submit;
- generated API client and shared schemas/design tokens;
- secure storage for refresh/session material;
- hosted API as the system of record.

Share contracts and design tokens, not arbitrary web UI components. Native interaction and store compliance take priority over superficial code sharing.

## Dependency acceptance rule

Before adding a production dependency, verify:

1. it solves an active milestone requirement;
2. it is maintained and compatible with target platforms;
3. it does not duplicate an existing dependency;
4. its license is compatible;
5. its transitive/security cost is acceptable;
6. removal or migration is plausible.
