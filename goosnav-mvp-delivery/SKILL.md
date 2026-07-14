---
name: goosnav-mvp-delivery
description: Turn a software idea or partial prototype into a real, launchable MVP with one shared service core, browser GUI and optional CLI adapters, deterministic fixture mode, customer-facing docs, cross-platform launch paths, a canonical verifier, and evidence-backed completion. Use when asked to build, finish, rescue, or ship an MVP without skeleton screens, fake integrations, or unverified claims.
version: 1.0.0
author: Goosnav LLC
license: Proprietary; internal use permitted
metadata:
  hermes:
    tags:
      - mvp
      - delivery
      - vertical-slice
      - verification
      - launchers
    related_skills:
      - goosnav-software-productization
      - goosnav-parent-verification
      - goosnav-local-first-workbench
---

# Overview

Deliver the smallest product that a real user can launch and use end to end. An MVP is not a folder tree, a persuasive README, or a collection of disconnected screens. It is one narrow job completed through production-shaped code, with safe defaults, a repeatable launch path, deterministic proof, and honest limitations.

Keep one domain/application core. The GUI, CLI, tests, fixture adapter, and future hosted surface call the same use cases rather than reimplementing behavior. Prefer a modular monolith and local browser GUI. Add infrastructure only when the accepted slice requires it.

The default completion contract is:

```text
input -> shared application service -> durable result -> visible GUI result
                                      -> CLI/JSON result when required
                                      -> exported artifact
```

Every arrow must run. A TODO, disabled button, hard-coded success response, or unexercised mock is not a completed arrow.

## When to Use

Use this skill when the user asks to turn an idea into an MVP, finish an incomplete application, make a prototype launchable, create a sellable first version, or prove a complete workflow. It is especially useful when multiple interfaces must agree, an AI/provider integration needs an offline demonstration mode, or prior agents created broad scaffolding without a usable happy path.

Do not use it merely to brainstorm product ideas or to plan distant scale. Use `goosnav-software-productization` when the primary problem is formal cross-platform packaging and gated commercial distribution. Use `goosnav-parent-verification` when implementation already exists and the main job is independent reconciliation.

## Workflow

1. **Define the one-sentence user contract.** Write: “For [specific user], the MVP turns [bounded input] into [valuable observable result] through [primary interface].” Name one happy-path example, completion signal, non-goals, and data/secrets boundary. If the statement contains “and” repeatedly, cut scope.

2. **Reconnoiter before changing code.** Read repository instructions, status, build manifests, lockfiles, entrypoints, routes, tests, and existing docs. Run the current launch and verifier if available. Record what actually works, what is missing, and which user changes must be preserved. Never infer completeness from filenames.

3. **Write a thin acceptance ledger.** Give each acceptance item an evidence source: command, browser action, file, screenshot, structured output, or fixture hash. Include launch from a clean-ish environment, the primary workflow, persistence/reopen where applicable, one expected failure, export, and shutdown. Mark unsupported platforms as untested rather than supported.

4. **Choose the smallest coherent architecture.** Put validation and business rules in the domain/application layer. Make UI routes and CLI commands adapters. Put persistence, filesystem, provider SDKs, clocks, randomness, and network access behind narrow ports. A direct function call is a valid port; do not manufacture frameworks or dependency injection containers.

5. **Create a deterministic fixture mode.** Fixture mode must exercise the same use case and output schema as the live adapter. Give it fixed inputs, fixed clock/seed when needed, visible `FIXTURE` labeling, and no network or credentials. It demonstrates product behavior and enables verification; it is never evidence of live provider success or market demand.

6. **Implement one vertical slice.** Start at the real launch surface, pass through the shared service, persist or export the result, and render it back to the user. Replace placeholders in that path. Make errors actionable. Avoid building secondary dashboards, auth, billing, plugin systems, or speculative abstractions until the primary slice passes.

7. **Make the GUI complete.** A default launch opens the useful browser page, not a blank shell or API docs. Include initial, loading, success, empty, validation-error, and operational-error states. Buttons must have handlers; forms must preserve or clearly reset state; browser refresh must have defined behavior. Bind local servers to loopback and protect state-changing routes.

8. **Add CLI parity only where valuable or required.** Map commands to the same application services. Document exit codes and offer stable machine-readable output such as `--json`. Do not create a separate batch implementation. A GUI-only MVP is valid when automation is not part of the user contract.

9. **Provide launchers and concise docs.** Supply native-feeling `install`/`run` entrypoints for supported developer platforms and a customer launch path proportionate to the request. Launchers resolve paths relative to themselves, surface failures, avoid credentials, and open the GUI. README instructions start with the exact launch command, primary workflow, data/export locations, recovery, and limitations.

10. **Create one canonical verifier.** A single command should compose fast static checks, domain tests, fixture integration, API/CLI contract checks, and a browser smoke or equivalent UI exercise. It must exit nonzero on failure, create temporary state outside the source tree, clean it, and print a concise evidence summary. Keep focused commands available for diagnosis.

11. **Run the no-skeleton audit.** Search for TODO/FIXME, `pass`, not-implemented exceptions, dummy success payloads, placeholder copy, disabled primary controls, sample-only routes, empty exports, and uncalled adapters. Classify each hit as test data, intentional deferred non-goal, or blocker. Remove generated databases, logs, screenshots, caches, and build noise unless they are deliberate evidence artifacts.

12. **Report evidence, then stop.** State the visible result, exact commands and outcomes, browser workflow observed, artifact paths/hashes when useful, fixture versus live coverage, untested platforms, and remaining limitations. “Complete” means every accepted item has observed evidence. External owner actions remain gated.

## Delivery Artifacts

Keep these small and repository-native:

- a customer/developer README with launch and recovery;
- a canonical verification command or script;
- safe deterministic fixtures and their provenance label;
- one representative exported artifact;
- tests around shared services and adapter contracts;
- launch scripts for platforms actually supported;
- a short evidence record, release note, or handoff.

Do not commit credentials, live customer input, warm caches, local databases, test screenshots by default, or generated artifacts that can be reproduced cheaply. Use temporary directories for verification.

## No-Skeleton Rules

- The primary button may not be disabled, unhandled, or backed by a hard-coded result.
- A route that returns success must perform or truthfully simulate the named operation.
- Fixture mode must be conspicuous and schema-compatible; it may not silently replace live mode.
- Export must produce a nonempty, reopenable artifact with declared schema/version when structure matters.
- CLI and GUI may format differently but may not disagree on domain rules.
- Docs must describe the current launch path, not an intended future architecture.
- A passing unit suite cannot substitute for launching the GUI and completing the job.
- Platform claims require native or appropriately isolated evidence.

## Pitfalls

- **Horizontal scaffolding:** models, repositories, API, UI, and tests all exist, but none connect. Recover by finishing one vertical slice and deleting unused seams.
- **Mock theater:** a canned result looks real. Label fixtures and keep live-adapter status separate.
- **Two cores:** GUI and CLI calculate or validate independently. Move the rule to one service and assert parity.
- **Warm-machine success:** launch relies on globally installed tools, hidden environment variables, or existing state. Verify with isolated temp data and documented prerequisites.
- **Verifier as a test dump:** hundreds of lines obscure the first failure. Keep a short summary and preserve detailed logs only when needed.
- **Scope laundering:** incomplete work is renamed “phase two” after implementation. Only defer items that were outside the accepted user contract or explicitly renegotiated.
- **Polish before behavior:** visual refinement hides missing actions. Get the workflow real, then perform visual QA.

## Verification Checklist

- [ ] The one-sentence user contract and non-goals are explicit.
- [ ] Default launch reaches the useful GUI without manual path repair.
- [ ] The primary workflow crosses one shared application core end to end.
- [ ] Fixture mode is deterministic, offline, visibly labeled, and contract-compatible.
- [ ] Live integrations are either exercised or honestly marked unverified.
- [ ] Initial, success, empty, validation, and operational-error UI states work.
- [ ] Persistence/reopen and export behavior match the contract.
- [ ] CLI output and exit codes are stable when CLI is in scope.
- [ ] The canonical verifier exits zero and a deliberate negative case exits nonzero.
- [ ] No blocking TODOs, placeholder handlers, dummy success paths, secrets, or generated noise remain.
- [ ] Exact commands, observed outcomes, limitations, and unsupported platforms are recorded.

## Exact Recipe

Recipe: deliver a local document-triage MVP from a partial Python repository.

1. Define the contract: “For an independent consultant, turn a folder of text fixtures into a reviewed priority list and export it as JSON through a local browser UI.” Keep live email ingestion, accounts, and hosted sync out of scope.
2. Run the existing tests and launch command; record their exit codes. Inspect routes and search for placeholders.
3. Implement `TriageDocuments.execute(request)` as the sole use case. Give it `DocumentSource`, `Clock`, and `PriorityPolicy` ports. Make the GUI route and `triage --json` command call it.
4. Add `fixtures/inbox-small/` containing non-sensitive invented documents. Fixture source returns them in stable order and the fixed clock is `2030-01-02T03:04:05Z`. Render a visible “Fixture data” badge.
5. Make the GUI import the fixture folder, allow priority edits, save a project manifest atomically, reload after restart, and export `triage-result.schema-v1.json`.
6. Add `scripts/verify.py` that checks formatting/static rules, runs domain tests, starts the server with a temporary data root, calls readiness, drives the primary browser flow, validates the exported JSON schema and nonempty items, then shuts down and deletes temporary state.
7. Run `python3 scripts/verify.py`, launch manually, perform import-edit-export-restart, and record the output artifact hash. Run once with an invalid input path and verify the UI explains the error without writing partial state.
8. Report fixture coverage separately from live ingestion: the MVP is complete for the accepted local-fixture contract; email ingestion remains unimplemented and is not implied.
