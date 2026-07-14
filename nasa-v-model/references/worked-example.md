# Worked Example — one fully-traced thread

The suite templates tell you *what* each document contains. This shows *what good looks like* by
following a single thread all the way down the left arm and back up the right arm, so the traceability
is visible end to end. It is deliberately tiny: one need, the requirements it spawns, the design that
satisfies them, and the verification that proves them. Real suites have dozens of these threads; they
all have this shape.

Product for the example: **Ledgerlight**, a local-first web app that turns a folder of bank-export
CSVs into a categorized monthly spending report. Single user, runs on their own machine.

---

## Left arm — descend from intent to detail

### ConOps need (doc 01)

> **N-003.** A user with several months of messy CSV exports wants one trustworthy monthly summary
> without hand-editing spreadsheets or uploading their finances to a third party.

Note it is stated in the user's terms, names the pain, and implies success criteria (trustworthy,
no third party). It carries an ID so everything below can point at it.

### System requirements (doc 02) — derived from N-003

| ID | Statement (`shall`) | Type | Parent | Method |
|---|---|---|---|---|
| SR-011 | The system shall import UTF-8 CSV files up to 25 MB and parse each row into a dated, signed amount without data loss. | Functional | N-003 | T |
| SR-012 | The system shall group transactions by calendar month and category and render a per-month total that reconciles to the sum of its rows to the cent. | Functional | N-003 | T |
| SR-NF-004 | The system shall perform all parsing and storage on the local device and make no outbound network request during import or reporting. | Privacy | N-003 | I |

Each is atomic, measurable, and testable. "Trustworthy" from the need became two concrete, checkable
claims (no data loss; totals reconcile to the cent). "No third party" became an inspectable
no-network requirement.

### Architecture / subsystem design (doc 03)

- **SS-IMPORT** — reads and validates CSV, normalizes rows. *Satisfies SR-011.*
- **SS-REPORT** — aggregates normalized rows by month/category, computes totals. *Satisfies SR-012.*
- **SS-STORE** — local SQLite file in the user's app-data dir; no network client is linked in.
  *Satisfies SR-NF-004.*

Tech choice justified against a requirement, not taste: SQLite (not a hosted DB) is chosen
*because* SR-NF-004 forbids sending data off-device.

### Component detailed design (doc 04) — one component of SS-IMPORT

> **CD-Parser-01.** `parse_csv(bytes) -> list[Row] | ParseError`
> - Rejects files > 25 MB before reading (streams size check).
> - Maps columns by header; on unknown schema returns `ParseError` with the offending header.
> - `Row = {date: ISO-8601, amount_cents: int (signed), description: str}`. Amounts parsed as
>   integer cents — never floats — so SR-012's cent-exact reconciliation is representable.
> - Requirements satisfied: SR-011. Est: ~120 LOC.

The float-to-cents decision is where a detailed-design choice is traced directly to a downstream
requirement (SR-012). That is the kind of reasoning the V is meant to surface early.

## Right arm — verify back up (plans written now, during design)

| ID | Verifies | Method | Environment | Pass/fail |
|---|---|---|---|---|
| VER-011 | SR-011 | T | CI, fixture CSVs | Import a 25 MB fixture and a malformed fixture; assert row count matches and `ParseError` names the bad header. Zero rows dropped. |
| VER-012 | SR-012 | T | CI | For each month, assert rendered total == sum(row.amount_cents). Off-by-a-cent fails. |
| VER-013 | SR-NF-004 | I | Review | Inspect the built bundle and run import under a blocked-network sandbox; any outbound socket fails the check. |
| VAL-003 | N-003 | D | Real user, real exports | User imports 3 months of their own CSVs and confirms the summary matches their own reckoning without editing spreadsheets. |

`VER-*` answer "did we build it right?" against the requirements. `VAL-003` answers "did we build the
right thing?" against the *need* — with the actual user and their actual data, which is the only
honest test of N-003.

## Traceability matrix row (doc 06)

| Need | Requirement | Satisfied by | Verified by | Method | Status |
|---|---|---|---|---|---|
| N-003 | SR-011 | SS-IMPORT / CD-Parser-01 | VER-011 | T | Open |
| N-003 | SR-012 | SS-REPORT | VER-012 | T | Open |
| N-003 | SR-NF-004 | SS-STORE | VER-013 | I | Open |

## Closure check (Phase 3)

- **Forward:** N-003 has three requirements. ✔
- **Backward:** every SR here names N-003 as parent. ✔
- **Verification:** every requirement has ≥1 activity with a method. ✔
- **Design:** every requirement maps to a subsystem/component, and no subsystem here exists without a
  requirement behind it. ✔

No orphans on this thread — it is closed. A real Phase-3 pass walks *every* thread this way and lists
any that fail to close in doc 06's open-items list.
