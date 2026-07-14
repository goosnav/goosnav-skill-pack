# Requirements, Verification Methods, and Traceability

This is the machinery that makes the suite trustworthy. Read it before writing the requirements doc
(02), the V&V plan (05), and the traceability matrix (06).

## Writing a good requirement

A requirement is a single, testable statement of something the system must do or be. Good requirements
share these properties (the INCOSE/NASA characteristics, in plain terms):

- **Atomic / singular.** One requirement per statement. If it contains "and" joining two capabilities,
  split it. You can't cleanly pass/fail a compound requirement.
- **Unambiguous.** One possible reading. Ban vague words -- "fast", "easy", "user-friendly", "robust",
  "efficient", "handle large files". Replace each with a measurable criterion ("renders the first
  screen in <= 1.5 s on an iPhone 12", "imports CSV files up to 50 MB").
- **Verifiable.** You can objectively demonstrate it's met (see verification methods below). If you
  cannot describe a test, the requirement is not done.
- **Necessary and traceable.** It exists because of a stated need (its parent). If no parent exists,
  either the need is missing from the ConOps or the requirement shouldn't exist.
- **Feasible and design-neutral (at the system level).** State *what*, not *how* -- leave the solution
  to the architecture/design docs, except where a constraint genuinely is a requirement (e.g., "shall
  run on iOS 16+").
- **Uses "shall".** Convention: "shall" = binding requirement, "should" = goal/preference, "may" =
  option, "will" = statement of fact about the environment. Use "shall" for every real requirement so
  they're greppable and unambiguous.
**Example -- weak vs strong**

Weak: `The app should load quickly and handle big files well.`
Strong:
- `SR-014: The system shall render the home screen within 1.5 seconds of cold launch on an iPhone 12 (iOS 16).`
- `SR-015: The system shall import comma-separated value files of up to 50 MB without data loss.`
Each strong requirement is atomic, measurable, and testable.

## The requirement ID scheme

Give every requirement a stable, unique, human-readable ID so it can be referenced from design docs,
tests, the traceability matrix, and code/commits. Recommended scheme:

- **Needs (ConOps):** `N-001`, `N-002`, ... (user needs / operational goals)
- **System requirements:** `SR-001` (functional), `SR-NF-001` (non-functional) -- or just `SR-###`
  with a "type" column. Keep it simple and consistent.
- **Subsystem requirements / design:** `SS-<subsystem>-001` (e.g., `SS-SYNC-001`).
- **Component design items:** `CD-<component>-001`.
- **Verification activities:** `VER-001` (verification), `VAL-001` (validation), or pair them to the
  requirement (`SR-014-T` for the test of SR-014).
IDs are permanent. If a requirement is removed, retire its ID -- don't reuse it. Number with leading
zeros so they sort. Keep the scheme documented in the SEMP (doc 00) so everyone uses it identically.

Each requirement entry should carry, at minimum:

| Field | Purpose |
|---|---|
| ID | Stable reference |
| Statement | The "shall" sentence |
| Type | Functional / Performance / Security / Privacy / Usability / Compliance / ... |
| Rationale | Why it exists (the need behind it) |
| Parent | The ConOps need ID (or higher requirement) it derives from |
| Verification method | T / A / I / D (below) |
| Priority | Must / Should / Could (or MoSCoW) |

## The four verification methods

NASA verifies every requirement by one of four methods. State which one applies to each requirement;
this forces you to confirm, at writing time, that the requirement *can* be checked.

- **Test (T).** Exercise the system with defined inputs and measure outputs against pass/fail criteria.
  The default for most software behavior. ("Run the import with a 50 MB CSV; assert zero row loss.")
- **Analysis (A).** Prove by calculation, modeling, or simulation when direct test is impractical.
  ("Model token cost per generation from measured prompt sizes to show it stays under $0.20.")
- **Inspection (I).** Examine the artifact directly -- read the code, the UI, the document. ("Inspect
  that no API key is present in the shipped client bundle.")
- **Demonstration (D).** Show the capability in operation without instrumented measurement. ("Demonstrate
  that the share sheet exports a generated file to Files.")
A requirement with no workable method is a smell -- rewrite it until one of the four clearly applies.

## The traceability matrix

The matrix is the spine that links the two arms of the V. It is a table (one row per requirement is
the usual orientation) with columns that let you walk both directions:

| Need (ConOps) | Requirement ID | Requirement (short) | Satisfied by (design) | Verified by | Method | Status |
|---|---|---|---|---|---|---|
| N-002 | SR-014 | Home screen <=1.5s cold launch | SS-UI, CD-Shell | VER-009 | T | Open |
| N-005 | SR-015 | Import CSV up to 50 MB | SS-IMPORT, CD-Parser | VER-010 | T | Open |

How to use it as a check (Phase 3 of the workflow):

- **Forward closure:** every `N-###` appears in the matrix with at least one requirement. A need with
  no requirement means the product won't meet a stated user goal -- flag it.
- **Backward closure:** every `SR-###` has a parent `N-###`. A requirement with no parent is either
  gold-plating (cut it) or evidence of a missing need (add it).
- **Verification closure:** every requirement has at least one verification activity and method. A
  requirement with no test cannot be proven met -- flag it.
- **Design closure:** every requirement maps to at least one design element that satisfies it, and
  every design element traces back to a requirement (no unjustified design).
Record the matrix as its own document (06). For large systems, generate it programmatically from the
requirement and design docs if they're structured (e.g., consistent ID tags) so it stays in sync.

## Tips for the two audiences

- **For Claude Code / agentic execution:** keep requirement IDs greppable, put the build order and an
  explicit ordered task list in the implementation doc, and make acceptance criteria literal enough to
  become test assertions. The agent should be able to pick a task, find its requirement ID, and know
  exactly what "done" means.
- **For a human team:** add rationale, estimates, staffing, and the approval path. Humans need to
  understand *why* and *how much*, not just *what*.
- **For both:** the same backbone serves both -- machine-actionable requirements are also the clearest
  ones for humans. You don't write two specs; you write one rigorous one.
