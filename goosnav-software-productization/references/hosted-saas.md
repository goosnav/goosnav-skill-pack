# Hosted SaaS architecture and operating model

## Recommended deployment topology

```text
Internet
  |
CDN / Web frontend (Vercel)
  |
FastAPI API containers (Railway)
  |---- Supabase Postgres
  |---- Supabase Auth
  |---- Supabase Storage
  |---- Redis -> Python workers
  |---- Stripe API/webhooks
  |---- AI provider APIs
  |---- Email provider
  |---- Sentry / logs / metrics

Owner Command Center -> same API, separate admin authorization policy
```

Do not host the Python API, workers, or secrets on GitHub Pages. A static site may host documentation or a marketing shell only.

## Environments

Maintain at least:

- local development;
- isolated staging with test billing/provider credentials;
- production.

Never share databases, storage buckets, secrets, OAuth callbacks, or Stripe webhook destinations between staging and production. Provide reproducible environment setup and a teardown procedure.

## Authentication

Default user-facing methods:

1. Google OAuth;
2. email OTP or magic link;
3. password only when product constraints require it.

Configure production SMTP, branded templates, redirect allowlists, session duration, and account recovery. Treat OAuth identity as authentication; map it to an internal user/tenant record and authorization policy.

## Data model minimum

Common entities:

- `users`
- `organizations` or `tenants` when collaboration/enterprise is required
- `memberships`
- `projects`
- `subscriptions`
- `entitlements`
- `usage_ledger`
- `quota_reservations`
- `jobs`
- `provider_requests`
- `audit_events`
- `support_events`

Do not use a single mutable “remaining uses” field without a ledger. Use append-only usage records plus derived balances. Reserve usage before costly work and reconcile actual cost afterward.

## Billing state machine

Stripe is the payment authority; the application maintains a synchronized entitlement projection.

Handle at minimum:

- checkout/session completion;
- subscription created/updated/deleted;
- trial ending;
- invoice paid;
- payment failed;
- disputed/refunded states where relevant;
- customer portal changes.

Requirements:

- verify webhook signatures;
- store processed event IDs and make handlers idempotent;
- tolerate out-of-order and repeated events;
- fetch authoritative objects when event context is insufficient;
- never grant durable access solely from a browser success redirect;
- define grace periods and downgrade behavior explicitly.

## Plans and entitlements

Default commercial shape:

- Tier 1: entry/basic model, low quota.
- Tier 2: primary offer, materially higher quota and better models/features.
- Tier 3: power/pro, highest self-serve quota and priority features.
- Enterprise: contact/quote, no public fixed price unless desired.

Store plan definitions in versioned configuration or tables, not scattered conditionals. Entitlements may include:

- allowed models;
- monthly credits/uses;
- max concurrency;
- project/storage limits;
- export/API/CLI access;
- support level;
- organization seats;
- feature flags.

A pricing page is marketing. The server-side entitlement policy is enforcement.

## Trial design

Preferred order:

1. no-AI interactive demo using deterministic/sample output;
2. BYOK trial;
3. verified-account limited trial with low-cost/free provider and hard budget;
4. preview flow that demonstrates setup and requests account/payment only before costly execution.

For any AI trial use verified identity, CAPTCHA/Turnstile, rate limits, device/IP signals, per-account quotas, idempotency, concurrency limits, anomaly detection, and a global kill switch.

## Background jobs

Move work to a queue when it is long-running, retryable, externally rate-limited, or should survive client disconnect.

Each job has:

- stable ID and idempotency key;
- tenant/user ownership;
- requested capability and reserved quota;
- bounded input references;
- status/progress;
- retry policy and dead-letter state;
- cancellation semantics;
- correlation/log ID;
- result reference and retention policy.

Never let a retry double-charge or duplicate a side effect.

## Owner command center

The command center is a protected administrative product, not a hidden collection of direct database edits.

Minimum capabilities:

- user/tenant search and status;
- subscription and entitlement view;
- quota adjustments with reason;
- provider/model enablement and cost caps;
- job queue status, retry, cancel, and dead-letter inspection;
- feature flags and maintenance mode;
- system health, error rates, latency, and cost summaries;
- support bundle/event lookup by correlation ID;
- account suspension/deletion/export workflows;
- enterprise lead inbox and booking handoff;
- immutable audit log for every admin mutation.

Use Stripe and Supabase dashboards during early operations, but do not make routine product support depend on SQL or service-role credentials.

### Multi-application integration contract

When operating multiple products, make each application expose an authenticated versioned control contract for:

- immutable application identity and deployed version;
- health and maintenance state;
- normalized subscriptions and entitlements;
- usage, provider cost, quota, and global/application kill-switch state;
- audited administrative commands and resulting events.

Make the central hub consume this contract. Do not grant it ad hoc direct database access to every product. Keep application-local authorization authoritative and make every remote mutation idempotent and audited.

### Digital-download storefront

Keep the M1a ZIP storefront operationally simple and separate from hosted application runtimes. Publish normalized product, order, refund, payment, and download-entitlement events to the hub contract. The storefront controls convenient paid access to files; it does not imply DRM inside M1a applications.

## Enterprise lead flow

Collect company, contact, use case, expected volume, security requirements, and desired date. Send a transactional email and create a CRM/support record. Calendar booking may use a scheduling link or API integration; do not expose private calendar credentials in the client.

## Production readiness

- custom domain and TLS;
- DNS records and email authentication;
- privacy policy, terms, support contact, and data-processing disclosures;
- database backup and restore test;
- storage lifecycle and deletion;
- migration/rollback process;
- error and budget alerts;
- dependency and container scanning;
- incident runbook and kill switches;
- load/concurrency test around the costliest workflow;
- launch checklist and owner dashboard.
