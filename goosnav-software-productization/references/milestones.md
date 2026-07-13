# Milestone definitions and acceptance gates

## M0 — M1a planning preflight

Treat M0 as a short internal preflight unless the user explicitly requests a separate architecture gate. Do not block a working local application behind document production.

Establish the target user, primary GUI workflow, non-goals, data/secrets boundaries, current launch path, supported matrix, M1a acceptance test, and coarse later roadmap. Then set M1a active.

## M1a — Universal ZIP application (default)

Use one customer ZIP with five stable launcher images and one mutable `app/` payload. Read `zip-app-architecture.md` before implementing this gate.

### Internal slices

1. Preserve the working GUI workflow and move changing product material beneath `app/`.
2. Define the manifest/bootstrap contract and loopback readiness behavior.
3. Generate stable Go supervisor images for macOS universal, Windows x64/ARM64, and Linux x86_64/ARM64.
4. Bundle pinned `uv` tools and configure locked, no-build, cross-platform production dependencies.
5. Implement versioned external runtimes, visible browser setup, retry/error handling, instance reuse, and child supervision.
6. Assemble the explicit-whitelist universal ZIP and exercise the failure matrix.
7. Produce clean-target evidence for every claimed OS/architecture.

### Gate evidence

- Extracting the ZIP exposes five clearly named launchers, `README.txt`, `LICENSE.txt`, and `app/` only.
- The appropriate image opens a browser setup page immediately, downloads managed Python/dependencies without developer tooling, and redirects to the working GUI.
- The primary workflow succeeds after first launch and restart; user data remains outside the release.
- Source, static, manifest, lockfile, and Python-version changes do not change launcher-image hashes.
- Lock/Python changes create a new ready runtime without damaging the prior one.
- Every failure maps to the documented stable code and leaves useful sanitized logs.
- All clean-target and exception cases in `zip-app-architecture.md` have actual evidence.

## M1b — Signed/offline packaged edition (optional)

Begin only after M1a is `USER_ACCEPTED` and the user explicitly continues.

Possible outcomes:

- Developer ID signing/notarization and Windows signing;
- installers or OS-native distribution wrappers;
- fully offline bundled runtime/dependencies;
- OS credential-store integration;
- automatic updates;
- optional licensing/activation only when explicitly required.

M1b passes when clean targets launch without developer prerequisites, complete and persist the primary workflow, update/remove cleanly, and reproduce the signed build.

## M2 — CLI and optional TUI

Map commands directly to application services. Document syntax, inputs, output schema, exit codes, side effects, overwrite/idempotency behavior, and noninteractive setup. Provide stable `--json`. Build a TUI only when it adds monitoring, iterative operation, browsing, or configuration value.

M2 passes when scripts consume documented output without parsing prose and GUI/CLI parity tests pass.

## M3 — Hosted ecosystem

### M3a: repeatable SaaS application foundation

Add tenant-aware storage, authentication/authorization, server-held provider keys, entitlements, quotas, usage/cost ledgers, hard caps, verified billing webhooks, jobs, backups, observability, privacy, and staging.

### M3b: central owner hub

Define an authenticated versioned integration contract for app identity, health, versions, subscriptions, entitlements, usage, cost, quota/kill-switch commands, and audit events. Make the hub use this contract instead of direct cross-application database access.

### M3c: digital-download storefront

Add a low-cost catalog/payment/download service for M1a ZIP products. Report products, orders, refunds, and download entitlements through the same hub contract. Keep it operationally separate from hosted application runtimes.

M3 passes only after tenant isolation, webhook replay, cost caps, backup restore, privileged audit, and staging promotion/rollback tests pass.

## M4 — Mobile

Build iOS/Android clients against the accepted hosted API. Cover session storage, deep links, offline/retry behavior, interruption safety, accessibility, privacy disclosures, store-compliant billing/account management, crash reporting, and physical-device evidence.
