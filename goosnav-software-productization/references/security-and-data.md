# Security, secrets, data, and local runtime

## Local secrets

The GUI may collect a user-supplied API key, and settings edits persist automatically. Persistence goes through a secret-storage adapter with these backends:

1. Zip Edition default: a permission-restricted config file (or `.env`) in the platform app-data directory — owner-only file permissions, never inside the repository, GUI-editable;
2. preferred upgrade, required from M1b packaging onward: operating-system credential vault/keychain, or an encrypted application store when a vault is unavailable;
3. environment variable for ephemeral automation;
4. repository `.env` only for developer/source mode.

Because storage is behind an adapter, upgrading from config file to keychain is a backend swap plus a one-time migration, not a rewrite.

Never display a stored secret after save. Provide replace, test, and delete actions. Redact secrets and likely token patterns from logs and support bundles.

## Hosted secrets

Provider keys, Stripe keys, webhook signing secrets, database service credentials, SMTP credentials, and signing material remain server-side in the host secret manager. Browser/mobile code may receive only public identifiers explicitly designed for clients.

Rotate secrets without code changes. Document scope, owner, environment, rotation method, and blast radius.

## Local server security

A browser-based local application can be attacked by malicious websites if its localhost API is permissive.

Required controls:

- bind only to `127.0.0.1`/`::1` unless LAN use is explicitly required;
- select or validate the port and avoid predictable privileged endpoints;
- use an unguessable per-launch session token between launcher/UI and backend;
- strict CORS allowlist; never `*` with credentials;
- validate `Origin` and use CSRF protections for state changes;
- do not put secrets in URLs;
- restrict file-system operations to approved roots and canonicalize paths;
- prevent arbitrary command execution through filenames or user input;
- terminate sidecar processes reliably;
- use timeouts, size limits, and cancellation.

If LAN access is a feature, treat it as a distinct milestone with authentication, TLS or a trusted tunnel, firewall guidance, and explicit opt-in.

## User data layout

Use a platform path resolver. Recommended logical layout:

```text
<AppData>/<Company>/<App>/
  config/
  secrets/          # only if not in OS vault; encrypted/restricted
  db/
  logs/
  cache/
  workspaces/
  exports/
  support/
```

Each project/workspace:

```text
<ProjectName>/
  project.json      # schema_version, id, name, created, modified, app_version
  inputs/
  outputs/
  assets/
  history/          # only if the product needs it
```

Use atomic writes, backups before migration, schema versions, and explicit import/export. Never trust project archives: validate paths and prevent zip-slip/path traversal.

## Logging

Use structured events with:

- timestamp, level, event name, component;
- application/version/build;
- request/job/correlation ID;
- safe operational fields;
- error class and sanitized message;
- optional stack trace in local debug logs.

Do not log secrets, full prompts by default, payment data, auth tokens, sensitive file contents, or unrestricted personal data. Rotate logs and cap disk usage. Make telemetry opt-in for the local paid edition unless the product contract clearly says otherwise.

A support bundle should be user-visible before export and include only:

- application/build/platform information;
- sanitized configuration summary;
- bounded recent logs;
- health checks;
- migration state;
- optional user-selected problematic file.

## Hosted authorization and multi-tenancy

Authentication answers “who.” Application authorization answers “may this identity perform this action on this resource.” Enforce authorization server-side for every operation.

- Every tenant-owned row has a tenant/user ownership key.
- Use Postgres row-level security when appropriate, but also maintain application-layer policy tests.
- Service-role credentials never reach clients.
- Admin access uses explicit roles, MFA where supported, and audit logging.
- Background jobs carry tenant context and re-check authorization/entitlement at execution time when needed.

## AI cost and abuse controls

Every costly operation requires:

1. authenticated or explicitly approved trial identity;
2. entitlement check;
3. idempotency key;
4. per-user/tenant rate and concurrency limit;
5. quota/credit reservation before provider call;
6. provider timeout and maximum token/output limits;
7. actual usage reconciliation after completion;
8. hard per-user, per-tenant, and global spend caps;
9. anomaly logging and kill switch.

IP rate limits are a secondary signal, not identity. Free provider models can disappear, throttle, change terms, or still impose infrastructure cost.

## Threat-model minimums

At each milestone evaluate:

- secret theft;
- malicious files and path traversal;
- prompt injection through imported content;
- arbitrary code/command execution;
- localhost cross-site attacks;
- dependency/supply-chain compromise;
- corrupted local database or interrupted migration;
- cross-tenant access;
- account takeover;
- billing/webhook forgery and replay;
- quota bypass and concurrency abuse;
- admin privilege misuse;
- mobile token extraction;
- privacy/data deletion failure.
