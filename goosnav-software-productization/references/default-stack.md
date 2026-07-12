# Default technical architecture

Use this stack as the default, not as dogma. Record every material deviation in `dev/DECISIONS.txt` with its constraint, cost, and migration impact.

## Architectural principle

Use a modular monolith with ports and adapters until measured evidence requires distribution.

```text
React web UI -------\
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
- `keyring` or a Tauri secure-store/keychain adapter for local secrets.
- `pytest`, Ruff, and a static type checker.

Use C++/Rust acceleration only behind a stable native boundary when profiling proves Python is materially inadequate. Provide deterministic tests comparing accelerated and reference implementations.

## Web UI

- React + TypeScript + Vite for the product application.
- Tailwind CSS plus shadcn/ui-style source components for a coherent, owned design system.
- TanStack Query for remote/server state.
- React local state/context first; add a client-state library only when justified.
- Zod or generated schemas at external boundaries.
- OpenAPI-generated TypeScript API client. Do not hand-maintain duplicate request/response types.
- Vitest for component/unit tests and Playwright for real browser workflows.

For a public marketing site requiring server-rendered SEO, add a separate Next.js site in M3. Do not force the product client into a server-rendered architecture merely for a landing page.

## Local desktop packaging

Default:

- Tauri 2 shell for Windows, macOS, and Linux.
- React/Vite assets in the WebView.
- FastAPI backend packaged per target as a sidecar executable with PyInstaller.
- Tauri starts the sidecar, waits for health, passes a one-time local session token, opens the application, and terminates the child on exit.
- Development mode may open the normal browser against the same backend.

Release artifacts are built separately per operating system and CPU architecture. Sign and notarize where commercially required.

Source-mode launchers:

- `start.command` for macOS convenience;
- `start.sh` for macOS/Linux shell use;
- `start.ps1` for Windows PowerShell;
- optional `.bat` wrapper for users who cannot run PowerShell scripts directly.

These launchers are not substitutes for packaged releases.

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
