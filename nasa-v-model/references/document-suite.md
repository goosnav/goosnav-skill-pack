# Document Suite Templates

Section-by-section templates for each document in the suite. Create each as a separate, numbered file
in the user's output folder. Adapt to the project -- omit sections that don't apply, add ones that do --
but keep the V backbone intact (ConOps, Requirements, Architecture, V&V, Traceability are mandatory).

Write in clear prose with numbered requirements where called for. Default to readable Markdown unless
the user asked for a specific format (`.docx`, `.pdf`, `.txt`); if so, read that output skill after
the content exists, then render. Cite current sources inline for any external fact.

---

## 00 -- Index & Systems Engineering Management Plan (SEMP)

- **Document map** -- the list of all docs, one line each, and the recommended reading order.
- **Purpose & scope** -- what this suite covers and explicitly does not.
- **Lifecycle model** -- the V, and where this project sits on it.
- **Roles & responsibilities** -- who owns what (for a human team) / which agent does what.
- **Conventions** -- the requirement ID scheme, "shall/should/may" usage, file naming, versioning.
- **Traceability policy** -- how links are maintained and how closure is checked before handoff.
- **Definition of done** -- the project-level success criteria, pointing forward to System Validation.

## 01 -- Concept of Operations (ConOps)

- **Vision** -- one paragraph: what this is and why it matters.
- **Users / personas** -- who they are, their skill level, their context.
- **Problem statement** -- the pain being removed, today's status quo.
- **Operational scenarios** -- 3-7 concrete user journeys, step by step, in the user's language ("a
  user opens the app, types ..., sees ..."). These become validation scenarios later.
- **Operating environment** -- devices, OS, connectivity, scale, constraints of the real setting.
- **Assumptions & dependencies** -- what must be true for the concept to hold.
- **Success definition** -- what success looks like *to the user* (concrete, measurable where possible).
  Tag the user needs with IDs (`N-001`, ...) -- these are the parents of all requirements.

## 02 -- System-Level Requirements

- **Functional requirements** -- numbered "shall" statements, grouped by capability area. Each with
  ID, statement, rationale, parent need, verification method, priority (see
  `requirements-and-traceability.md`).
- **Non-functional requirements** -- performance, reliability, security, privacy, accessibility,
  localization, observability -- same format, measurable thresholds.
- **Constraints** -- platform, regulatory, budget, timeline, mandated/forbidden tech.
- **External interfaces** -- third-party APIs/SDKs the system must talk to, with the contract.
- Present as a table or structured list so each requirement is individually addressable.

## 03 -- System Architecture & Subsystem Design (High-Level Design)

- **Architecture overview** -- a diagram (ASCII/Mermaid) and narrative of the major subsystems and how
  data/control flows between them.
- **Subsystem breakdown** -- for each subsystem: responsibility, the system requirements it satisfies
  (by ID), its interfaces, and its key design decisions.
- **Technology stack** -- each major choice justified against a requirement or constraint (not taste).
- **Data model** -- entities, relationships, storage, and lifecycle.
- **Interface definitions** -- the contracts between subsystems and to the outside world.
- **Platform-specific design** -- where targets differ (e.g., iOS vs Android behavior), call it out
  explicitly; this is where compliance-driven divergence lives.
- **Cross-cutting concerns** -- security model, error handling strategy, logging/telemetry.

## 04 -- Component Detailed Design

For each component within each subsystem:

- **Responsibility** -- the single job of this component.
- **Interface / contract** -- inputs, outputs, function/endpoint signatures, error cases.
- **Data structures** -- the shapes it owns or passes.
- **Algorithm / logic** -- enough that an engineer or Claude Code can implement with no further design.
- **Dependencies** -- what it relies on (other components, libraries).
- **Requirements satisfied** -- the IDs it implements.
- **Estimates** (when requested) -- approx lines of code and effort, with a range, so totals roll up to
  the project estimate in doc 07.

## 05 -- Verification & Validation Plan

Structured to mirror the right arm of the V, written now (during definition):

- **Component verification procedures** -- per component, the unit/integration tests and pass/fail
  criteria that prove it meets its detailed design.
- **Subsystem verification plan** -- how assembled subsystems are tested against subsystem requirements.
- **System verification plan** -- how the integrated system is tested against every system-level
  requirement; reference each requirement ID and its method (T/A/I/D).
- **System validation plan** -- how the finished product is checked against the ConOps scenarios and
  success definition ("did we build the right thing?"), ideally with real or representative users.
- For each activity: ID, the requirement(s)/need(s) it covers, method, environment, pass/fail criteria.

## 06 -- Traceability Matrix

The closure table linking needs -> requirements -> design -> verification, bidirectionally (format and
closure checks in `requirements-and-traceability.md`). Include a short "open items" list at the bottom
naming every orphan found so they're impossible to miss.

## 07 -- Implementation & Build Plan

- **Build order / sequencing** -- what gets built first and why (dependency order, riskiest-first, or
  thinnest-end-to-end-slice-first).
- **Milestones** -- grouped deliverables with rough timing.
- **Environment & tooling** -- repos, CI, test harness, branching, secrets handling.
- **For agentic execution** -- an explicit, ordered task list Claude Code can pick up, each task naming
  the requirement IDs it implements and its acceptance criteria.
- **For human teams** -- staffing plan, team size, timeline, and total effort rolled up from doc 04
  estimates.

## 08 -- Approval / Compliance / Go-to-Market (when relevant)

- **Per-platform approval path** -- e.g., App Store and Google Play review requirements, the specific
  guidelines that apply, and how the design satisfies them. Cite the *current* rules with sources and
  dates -- these change often and are frequently decision-changing.
- **Legal & privacy** -- data handling, privacy policy, terms, age ratings.
- **SDK/API commercial terms** -- licensing and usage limits of anything the product is built on.
- **Launch checklist** -- the concrete steps from "code complete" to "live".

## 09 -- Risk Register & Open Questions

- **Risk register** -- a ranked table: risk, likelihood, impact, exposure (likelihood x impact),
  mitigation, owner. Order by exposure.
- **Open questions** -- the small set of decisions that must be resolved *before* coding starts (naming/
  trademark, unverified pricing, ambiguous requirements, legal sign-off). Be honest and specific.

## (optional) Business & Unit Economics

When viability depends on it: cost drivers, unit cost per key action (with current, cited pricing),
pricing tiers, and the path to the user's revenue goal. Recommend a leaner first slice if the full
build's cost dwarfs the stated business goal -- same architecture, smaller scope -- so nothing is wasted.