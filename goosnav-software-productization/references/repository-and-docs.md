# Repository structure and durable project documents

## Mature target layout

Create directories only when their milestone begins; do not fill the repository with speculative implementations.

```text
/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── SETUP.txt
├── LICENSE.txt
├── .env.example
├── .gitignore
├── dev/
│   ├── STATE.txt
│   ├── NORTHSTAR.txt
│   ├── SOFTWARE_BIBLE.txt
│   ├── ARCHITECTURE.txt
│   ├── TECH_STACK.txt
│   ├── ROADMAP.txt
│   ├── SPRINT_PLAN.txt
│   ├── DECISIONS.txt
│   ├── TEST_PLAN.txt
│   ├── THREAT_MODEL.txt
│   └── RELEASE_CHECKLIST.txt
├── apps/
│   ├── web/               # M1/M3 product client
│   ├── desktop/           # M1 Tauri shell
│   ├── admin/             # M3 owner command center
│   └── mobile/            # M4 Expo application
├── services/
│   ├── api/               # FastAPI transport/composition
│   └── worker/            # M3 jobs
├── packages/
│   ├── core/              # Python domain/application services
│   ├── persistence/       # repositories and migrations
│   ├── providers/         # AI/external adapters
│   ├── cli/               # M2
│   ├── tui/               # M2
│   ├── api-client/        # generated TypeScript client
│   ├── ui/                # web design system
│   └── design-tokens/     # cross-surface tokens
├── scripts/
├── tests/
└── .github/workflows/
```

A smaller project may use fewer directories, but retain the same boundaries. Do not create one giant `app.py` that owns transport, business logic, persistence, provider calls, and file paths.

## Document ownership

### AGENTS.md

Operational rules that Codex and other agents read automatically. Keep it concise. Include:

- active milestone rule;
- required documents to read;
- canonical setup/build/test/run commands;
- architecture boundaries;
- prohibited secret/data locations;
- completion and documentation requirements.

### CLAUDE.md

Bridge for Claude Code. Prefer a short file that instructs Claude to read and follow `AGENTS.md` and the active `dev/` documents. Avoid maintaining two divergent rulebooks.

### NORTHSTAR.txt

Stable user experience:

- who the user is;
- what they are trying to accomplish;
- what “effortless” means;
- the primary happy path;
- acceptable and unacceptable failure behavior;
- quality bar.

### SOFTWARE_BIBLE.txt

Durable product semantics:

- vocabulary and entities;
- rules and invariants;
- workflows;
- permissions;
- persistence behavior;
- defaults;
- non-goals;
- compatibility promises;
- known product decisions.

It is not a sprint backlog.

### ARCHITECTURE.txt

Use C4-like context/component descriptions plus data flows and trust boundaries. Include:

- module responsibilities;
- dependency direction;
- API contracts;
- persistence and file layout;
- process lifecycle;
- local vs cloud adapters;
- failure modes;
- deployment topology by milestone.

### TECH_STACK.txt

Record chosen tools and why. Include version policy, lockfiles, supported OS/architectures, build tools, and approved deviations from the protocol default.

### ROADMAP.txt

One page per milestone at most. State outcome, dependencies, risks, and exit gate. Future milestones remain coarse.

### SPRINT_PLAN.txt

Only the active milestone is detailed. Use checkable vertical slices and acceptance evidence. Archive completed plans if useful rather than endlessly appending.

### DECISIONS.txt

Append-only ADR-style entries:

```text
DECISION-YYYYMMDD-NNN: Title
STATUS: Proposed | Accepted | Superseded
CONTEXT:
DECISION:
CONSEQUENCES:
ALTERNATIVES REJECTED:
REVERSAL TRIGGER:
```

### STATE.txt

Machine- and human-readable control plane for the development protocol. Keep the first fields stable:

```text
PROTOCOL: GSPP
PROTOCOL_VERSION: 1.0.0
CURRENT_MILESTONE: M1
STATUS: ACTIVE
LAST_USER_ACCEPTED_MILESTONE: M0
NEXT_ALLOWED_MILESTONE: M1
CURRENT_SLICE: M1-S03
LAST_UPDATED: 2026-07-11
```

### TEST_PLAN.txt

Map requirements and risks to unit, contract, integration, end-to-end, packaging, security, performance, and manual acceptance tests.

### THREAT_MODEL.txt

Track assets, actors, entry points, trust boundaries, misuse/abuse cases, mitigations, residual risk, and security tests. Update materially at M1 packaging, M2 automation, M3 multi-tenancy/billing, and M4 mobile.

### RELEASE_CHECKLIST.txt

Evidence, not aspirations. Include artifact checksums, CI run, supported platforms, migration version, signatures/notarization, smoke tests, known issues, rollback, and user acceptance status.

## Git rules

- Commit source, tests, migrations, safe fixtures, docs, CI, and lockfiles.
- Never commit `.env`, API keys, credential stores, production dumps, user projects, logs, caches, local databases, uploads, support bundles, build artifacts, or signing keys.
- Provide `.env.example` with names, descriptions, and safe placeholders.
- Keep generated API clients committed only when that improves reproducibility; verify they match the source schema in CI.
- Use Git LFS only for intentional versioned assets, not user-generated data.
- Protect the primary branch and require passing CI for releases.
