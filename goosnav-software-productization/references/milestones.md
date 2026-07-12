# Milestone definitions and acceptance gates

## M0 — Product contract and architecture

### Deliverables

- Target user, pain, desired outcome, and primary job.
- One-sentence product promise.
- Primary workflow and failure/recovery workflow.
- Functional requirements and explicit non-goals.
- Data classification and retention assumptions.
- Local/SaaS/mobile commercialization thesis.
- Architecture context/component/data-flow diagrams.
- M1a acceptance test written from the user's perspective.

### Gate evidence

- No unresolved contradiction between North Star, software bible, architecture, and roadmap.
- Critical external dependencies and costs identified.
- M1 scope can fit into coherent vertical slices.

## M1 — Local edition

M1 splits into M1a (Zip Edition, required and sellable) and M1b (Packaged Edition, a deferrable polish upgrade). After M1a is `USER_ACCEPTED`, the user chooses: build M1b now, or mark it `DEFERRED` and proceed to M2.

### M1a Zip Edition — internal sub-stages

1. Walking skeleton: browser UI -> local API -> persistence -> restart.
2. Primary workflow: full user value, not placeholder screens.
3. Reliability: migrations, errors, logs, recovery, tests.
4. Configuration: settings, GUI-editable BYOK provider setup, validation, health checks.
5. User projects: create/open/rename/archive/export with versioned manifests as applicable.
6. Launchers and wizard: `start.command`/`start.sh`/`start.ps1`, iconed top-level launcher, idempotent first-run dependency wizard.
7. Zip release: clean-machine smoke tests and a top-level tutorial covering API-key acquisition and setup.

### M1a gate evidence

- `git clone` plus documented developer setup succeeds.
- On a clean machine or clean user account: extract zip, double-click launcher, wizard completes with no manual steps, app opens in the browser.
- Main workflow succeeds after first run and after restart.
- Re-running the launcher after an interrupted wizard resumes cleanly.
- Corrupt/missing configuration yields recoverable guidance.
- Secrets do not appear in logs, repo, crash reports, or support bundle.
- A user can locate, export, and back up their projects.
- Version and migration behavior is documented.

### M1b Packaged Edition — internal sub-stages

1. Tauri shell, PyInstaller sidecar, health/handshake lifecycle.
2. Icons, installers/artifacts per OS and architecture.
3. Secrets migrated to the OS credential store or Tauri secure store.
4. Cross-platform release: CI matrix, clean-machine smoke tests, signing/notarization where required.

### M1b gate evidence

- Packaged release launches with no preinstalled runtime and no wizard.
- Main workflow succeeds after install and after restart.
- Uninstall/removal is clean.
- Build reproduces from source on CI.

## M2 — Automation edition

### CLI contract

Each command documents:

- syntax and examples;
- inputs and precedence (flag, environment, config, prompt);
- output schema;
- exit codes;
- side effects;
- idempotency/overwrite behavior;
- log and diagnostics location.

Suggested global flags:

- `--config`
- `--project`
- `--json`
- `--quiet`
- `--verbose`
- `--no-color`
- `--non-interactive`
- `--version`

Do not require interactive prompts when all values can be passed explicitly.

### TUI acceptance

Only implement if it improves monitoring, iterative operation, browsing, or configuration. It should expose keyboard help, focus/navigation, progress, cancellation, status, and logs. It should survive terminal resizing and degraded color environments.

### Gate evidence

- GUI and CLI parity test for every shared primary workflow.
- Shell automation consumes JSON output without parsing prose.
- Failures return nonzero stable exit codes.
- CLI can configure secrets through a secure mechanism without echoing them.

## M3 — SaaS edition

### Internal sub-stages

1. Cloud architecture and threat model.
2. Staging deployment and tenant model.
3. Authentication and authorization.
4. Core workflow against cloud data/storage.
5. Usage metering, quotas, and cost controls.
6. Stripe billing and entitlement state machine.
7. Background jobs, retries, and idempotency.
8. Owner command center.
9. Privacy, account lifecycle, support, backup/restore.
10. Production launch and rollback.

### Gate evidence

- Cross-tenant access tests fail closed.
- Stripe webhook replay is idempotent.
- Payment cancellation/failure revokes or degrades access correctly.
- Usage cannot exceed both plan and global spend caps.
- Provider key never reaches browser/mobile clients.
- Backup restore is rehearsed.
- Staging can be promoted or reproduced from infrastructure configuration.
- Admin actions are authorized and audited.

## M4 — Mobile edition

### Internal sub-stages

1. Mobile product decision and store-policy review.
2. Navigation/design system and API client.
3. Auth/session/deep-link flow.
4. Primary workflow on device.
5. Offline, retry, upload/download, and interruption behavior.
6. Mobile purchase/account flow.
7. Accessibility, privacy, telemetry, support.
8. TestFlight/closed test and store submission.

### Gate evidence

- Primary workflow works on physical iPhone and Android hardware.
- Session survives normal lifecycle and expires safely.
- Network interruption does not corrupt state or duplicate paid/costly operations.
- Current store rules are documented with review date.
- Account deletion and subscription management are reachable and compliant.
- Production-signed builds and store assets exist.
