---
name: nasa-v-model
description: >-
  Produce a complete, traceable specification suite for a software product or system using NASA's
  Systems Engineering "V" model (ConOps to requirements to architecture to detailed design on the
  way down; component, subsystem, and system verification and validation on the way up, with
  traceability throughout). Use this skill whenever the user wants to spec out, plan, architect, or design a new
  app, product, feature, or system before building it -- especially when they say things like "write
  the specs", "app bible", "build to spec", "PRD", "design doc", "systems engineering", "V-model",
  "requirements doc", "hand this to a dev team", "hand this to Claude Code", or want a rigorous,
  buildable plan rather than just code. Also use it when someone has a rough product idea and wants
  it turned into something a team (human or agentic) can execute end-to-end. Trigger even if the user
  doesn't name the V-model by name -- if they want a serious, complete, verifiable spec, use this.
---

# NASA V-Model Specification Suite

## What this skill is for

Turn a product idea into a **complete, internally consistent, traceable specification suite** that a
team -- human engineers, an agentic coder like Claude Code, or both -- can execute to a shipped
product with no unanswered questions. The output is a set of documents structured on NASA's Systems
Engineering "V" model. The defining feature of a good result is not length; it is **traceability and
verifiability**: every requirement traces up to a user need and down to a design element and a test,
and every requirement is written so you can objectively prove it was met.

This skill is for the *specification* phase. It does not write the production app. It produces the
artifacts that make writing the app boring and predictable.

## The V model in one picture

The "V" reads left-to-right over time. The **left arm** decomposes the problem from intent down to
detail. The **bottom** is implementation. The **right arm** integrates and tests back up, and each
right-side activity verifies against the left-side document at the same height. The plans for the
right side are written *while descending the left side* -- this is the whole point of the V.

```
Definition & Decomposition (down)              Integration & Test (up)
  ConOps  ........... System Validation Plan ......... System Validation
  System Requirements ... System Verification Plan ... System Verification
  Subsystem Requirements . Subsystem Verif. Plan ..... Subsystem Verification
  Component Detailed Design . Component Verif. Proc. .. Component Verification
                 \                                    /
                  Implementation (code + unit test)
                            <- Traceability binds both arms ->
```

Mapping to documents (left height -> right height):

| Left arm (define) | Paired plan (write on the way down) | Right arm (verify on the way up) |
|---|---|---|
| Concept of Operations | System Validation Plan | System Validation ("did we build the right thing?") |
| System-Level Requirements | System Verification Plan | System Verification ("did we build it right?") |
| Subsystem Requirements / High-Level Design | Subsystem Verification Plan | Subsystem Verification |
| Component Detailed Design | Component Verification Procedures | Component Verification |

Over the whole thing sits the **Systems Engineering Management Plan (SEMP)** -- how the project is run
-- and **traceability** runs through everything.

For the deeper explanation of each level, read `references/v-model.md`.

## Workflow

Follow these phases in order. Do not skip the clarification and research phases -- a beautiful spec
built on wrong assumptions is worse than no spec, because a team will execute it faithfully.

### Phase 0 -- Clarify intent and scope

Before writing anything, pin down what you're specifying. If the user has already given a rich brief
(or there's a prior conversation describing the product), extract answers from it first and only ask
about real gaps. Use the question tool if available; otherwise ask inline. You need to know:

- **The product and its job.** What is it, who is it for, what problem does it remove?
- **Primary consumer of the specs.** A human dev team, an agentic coder (Claude Code), or both. This
  changes emphasis: human teams need readability, estimates, staffing, and approval paths; agentic
  coders need machine-actionable, unambiguous, testable requirements and explicit build order. "Both"
  means do all of it.
- **Platforms / deployment targets** (iOS, Android, web, backend, embedded, etc.) -- these drive the
  architecture and any compliance/approval path.
- **Constraints that change the design**: budget, timeline, team size, business model, regulatory or
  app-store rules, must-use or must-avoid technologies.
- **Definition of done / success metrics.** How will the user know the built thing succeeded?
- **Output depth.** Default to the full suite (below). Offer a lighter single-doc version if the user
  wants speed over completeness.

### Phase 1 -- Research current facts FIRST

Specs contain claims that must be true *today*: pricing, SDK/API capabilities, platform store rules,
library versions, regulatory constraints, competitor existence. These drive real numbers and real
go/no-go decisions, and they change constantly. Before drafting, **search the web and fetch primary
sources** for every such fact the spec will rely on. Note dates and cite sources inside the docs.

A spec that says "Apple allows X" or "this API costs $Y" without a current source is a liability.
When a finding is decision-changing (e.g., a platform rule that breaks the proposed architecture),
surface it to the user plainly before building the suite around it.

If an output-format skill is needed for the deliverable (e.g., `docx`, `pdf`), read that skill's
SKILL.md only *after* research is complete, then build the formatted files.

### Phase 2 -- Generate the document suite (descend the left arm)

Create the documents below as **separate files** in the user's output folder, numbered so the reading
order is obvious. Write them top-to-bottom of the V; each level derives from the one above it. Do not
invent design before there's a requirement to justify it, and do not write a requirement you can't
later verify.

Keep prose readable for humans **and** precise for machines: every requirement is a numbered "shall"
statement with a stable ID and a verification method. See `references/requirements-and-traceability.md`
for the ID scheme, requirement-quality rules, the four verification methods, and the traceability
matrix format. See `references/document-suite.md` for the section-by-section template of every doc.
See `references/worked-example.md` for a single need traced all the way down and back up -- read it
once to calibrate what "closure" looks like before writing your own threads.

The standard suite (adapt numbering/contents to the project):

- **00 -- Index & SEMP.** Map of all documents and how to read them; the Systems Engineering
  Management Plan: lifecycle, roles, conventions, the requirement ID scheme, the traceability policy,
  and the definition of done. This is the front door.
- **01 -- Concept of Operations (ConOps).** Who the users are, the problem, operational scenarios /
  user journeys, the operating environment, and what success looks like in the user's terms. No
  solution detail -- this is intent. It is the validation baseline.
- **02 -- System-Level Requirements.** Functional and non-functional requirements as testable "shall"
  statements, each with an ID, rationale, parent (a ConOps need), and verification method. Includes
  performance, security, privacy, accessibility, and compliance requirements.
- **03 -- System Architecture & Subsystem Design (High-Level Design).** The decomposition into
  subsystems, the chosen tech stack (with justification tied to requirements), interfaces between
  subsystems, data model, and any platform-specific design (e.g., per-OS differences). Each subsystem
  states which system requirements it satisfies.
- **04 -- Component Detailed Design.** Per-component specs: responsibilities, interfaces/contracts,
  data structures, algorithms, error handling, and **build estimates** (approx lines of code and
  effort per component) when the user wants estimates. This is the level Claude Code or an engineer
  builds directly from.
- **05 -- Verification & Validation Plan.** The right arm, written now: component verification
  procedures, subsystem verification plan, system verification plan, and the system validation plan --
  each tied to the matching left-arm document. State the method, the pass/fail criteria, and the
  environment for each. This is what proves the build is correct and correct-for-purpose.
- **06 -- Traceability Matrix.** The spine. A table linking ConOps need -> system requirement ->
  subsystem/component -> verification activity, bidirectionally. Every requirement must appear with a
  parent and at least one verifying test; flag any orphans (requirement with no need, or need with no
  requirement, or requirement with no test).
- **07 -- Implementation & Build Plan.** Build order / sequencing, milestones, environment setup,
  branching/CI expectations, and -- for agentic execution -- explicit, ordered tasks Claude Code can
  pick up. For human teams: staffing, timeline, and dependency ordering.
- **08 -- Approval / Compliance / Go-to-Market path** (when relevant). The concrete path to ship:
  app-store review requirements per platform, legal/privacy review, licensing/commercial terms of any
  SDK used, and any regulatory steps. Cite current rules with sources.
- **09 -- Risk Register & Open Questions.** Ranked risks with likelihood, impact, and mitigation; plus
  the small set of decisions that must be resolved *before* code starts. End every suite with this --
  honesty about what's unresolved is part of the deliverable.
- **(optional) Business & Unit Economics** -- cost model, pricing, margins -- when the product's
  viability depends on it. Use current, cited pricing.
Not every project needs all of these, and some need extras (e.g., a data-migration plan, an API
reference). Scale the suite to the system, but never drop ConOps, Requirements, Architecture,
V&V, or Traceability -- those four-plus-spine are the V.

### Phase 3 -- Verify the spec against itself (ascend the right arm, on paper)

A spec suite has its own "right arm": before handoff, check internal consistency.

- **Traceability closes.** Walk the matrix. Every ConOps need has >=1 requirement; every requirement
  has a parent need, a design element, and a verifying test. Fix or flag every orphan.
- **Requirements are verifiable.** Re-read each "shall" and confirm a tester could objectively pass/
  fail it. Replace vague words ("fast", "user-friendly", "robust") with measurable criteria.
- **No contradictions.** The architecture doesn't violate a requirement; the build plan doesn't assume
  something the design forbade; estimates roughly add up to the stated timeline/budget.
- **Facts are current and cited.** Every external claim has a dated source.
Do this verification step explicitly -- ideally as a final pass listed in your task list, or via a
subagent for high-stakes specs. Then summarize for the user: what was produced, the headline numbers,
any decision-changing findings, and the open questions that gate the start of coding.

## Operating principles (the "why")

- **Traceability is the product.** The reason teams trust a spec is that nothing is arbitrary -- every
  line of design and every test exists because a requirement demanded it, and every requirement exists
  because a user need demanded it. If you can't trace it, cut it or question it.
- **Write requirements you can prove.** A requirement that can't be objectively verified isn't a
  requirement, it's a wish. The discipline of attaching a verification method to each one forces
  clarity at the moment of writing, which is when it's cheapest.
- **Define the tests while you define the need, not after.** Writing the validation/verification plan
  on the way *down* catches ambiguous or untestable requirements immediately -- that early feedback is
  the core value of the V over a waterfall.
- **Decompose, don't leap.** Intent (ConOps) -> what (requirements) -> how, broadly (architecture) ->
  how, exactly (detailed design). Each step is small and justified by the one above. Skipping levels is
  how specs end up with design decisions nobody can explain.
- **Current facts over confident memory.** Pricing, platform rules, and SDK capabilities move. Search
  and cite; don't assert from training knowledge.
- **Honest over impressive.** A right-sized spec that admits open questions and real costs beats an
  exhaustive one that hides them. Don't pad. If the "best version" is far more expensive than the
  user's goal justifies, say so and recommend a leaner path that uses the same architecture.

## Reference files

- `references/v-model.md` -- full explanation of each V level and the paired verification plans.
- `references/requirements-and-traceability.md` -- requirement-quality rules, the ID scheme, the four
  verification methods (Test / Analysis / Inspection / Demonstration), and the traceability matrix
  format. Read before writing documents 02, 05, and 06.
- `references/document-suite.md` -- section-by-section templates for every document in the suite. Read
  before Phase 2.
- `references/worked-example.md` -- one need traced down to detailed design and back up through
  verification, with a closure check. Read once to see what a closed thread looks like.
