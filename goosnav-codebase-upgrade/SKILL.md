---
name: goosnav-codebase-upgrade
description: Upgrade a partially working MVP or inherited codebase into a robust, secure, fast, user-effective, and GitHub-ready product through adversarial health audits, real user-journey and screenshot evidence, specialist-agent repairs, independent verification, and truthful documentation. Use when asked to harden, polish, rescue, audit-and-fix, productionize, or prepare an existing repository for release without replacing it with an exotic rewrite.
---

# Goosnav Codebase Upgrade

Upgrade the repository that exists. Find what is broken, silent, misleading, unsafe, slow, inaccessible, or inconsistent with the user's goal; repair the smallest credible root causes; and prove the final combined tree. Assume every completion claim is unverified until reproduced.

This is an implementation skill, not a report-only audit. Fix in-scope defects and finish the accepted upgrade. Reserve architectural replacement, framework migration, and speculative scale work for next steps unless the current user contract cannot be made safe and functional locally.

## Core rules

- Make the end user's job the primary acceptance contract. Code quality scores support that contract; they do not replace it.
- Begin from failure hypotheses. Look for dead controls, swallowed exceptions, canned success, stale state, partial writes, unsafe defaults, misleading docs, and paths tests never exercise.
- Treat automated checks as leads. Inspect raw logs, skipped checks, tool errors, configuration, reachability, and false positives.
- Inspect every D, E, and F complexity result. Inspect C whenever it touches a primary journey, trust/data/money boundary, high-churn code, or weak coverage. Do not refactor only to improve a letter grade.
- Preserve user changes and repository-native architecture. Prefer a local repair plus regression evidence over a new framework or generalized abstraction.
- Delegate implementation effort, never responsibility. The parent owns shared contracts, final integration, evidence, and the completion claim.
- Never call a missing, skipped, blocked, stale, or unavailable check a pass.

Read [references/evidence-and-grading.md](references/evidence-and-grading.md) before triage or completion. Read [references/specialist-contracts.md](references/specialist-contracts.md) before spawning specialists.

## Workflow

### 1. Freeze authority and repository state

Read repository instructions, current status and diff, manifests, lockfiles, entrypoints, tests, CI, deployment files, and documentation. Identify user-owned dirty paths and generated noise. Do not clean or rewrite them by assumption.

Confirm the allowed environment and external-action boundary. Auditing and tests can execute untrusted repository code. Do not expose production credentials, customer data, or a privileged network. Use isolated temporary state, loopback services, invented fixtures, bounded processes, and owner approval for destructive, paid, publishing, deployment, or live-production actions.

Record the baseline commit/tree state, supported runtime, documented launch command, canonical verifier, and the exact failure state before editing.

### 2. Define the user contract and acceptance ledger

Write one sentence:

```text
For <specific user>, this product turns <bounded input> into <valuable observable result>
through <primary interface>, complete when <visible completion signal>.
```

List three to seven critical journeys, including the primary happy path and meaningful failure/recovery paths. Include persistence/reopen, import/export, authentication/authorization, or live-provider behavior only when the product promises them.

Create one issue and acceptance ledger:

```text
ID | user journey/asset | severity | observed evidence | expected behavior
root cause/confidence | affected contract | owner/allowed paths | acceptance check
status | disposition/residual risk
```

Use `OBSERVED`, `INFERRED`, `CLAIMED`, and `UNVERIFIED` precisely. A plausible explanation remains inferred until reproduced.

### 3. Establish the evidence baseline

Run the repository's documented launch and canonical checks before generic tools. Capture exact command, working directory, tree state, exit code, and relevant artifact/log. A failing baseline is useful evidence, not permission to lower the bar.

Run the bundled collector from an isolated output directory:

```bash
bash <skill-directory>/scripts/codebase-audit.sh --source <repository>
```

The collector does not install tools. It writes a fresh run, records `PASS`, `FINDINGS`, `FAIL`, `ERROR`, and `SKIPPED`, and may exit 1 or 2 precisely because it found problems. Read `summary.md`, `status.tsv`, `context.txt`, and the raw logs. The final banner is never acceptance evidence.

Run `--run-tests` only after inspecting the repository and isolating state because tests execute repository code. Use `--allow-network` only when network access is authorized and advisory freshness matters. Prefer project-native environments and lockfile-aware commands over globally resolved tools. Rerun every essential command directly so its actual output and exit code are independently visible.

Do not install a pile of analyzers merely to fill the manifest. First use repository-native lint, format, type, build, test, dependency, and security commands. Record unavailable coverage as `UNVERIFIED` and compensate with semantic inspection or a proportionate alternative.

### 4. Launch read-only specialist reconnaissance

When subagents are supported and authorized, spawn at least three independent read-only specialists. Keep the parent active and stay within the concurrency limit:

1. runtime correctness, tests, state, error handling, and C–F hotspot specialist;
2. end-user workflow, browser, screenshot, accessibility, and customer-value specialist;
3. application security, dependency/supply-chain, secrets, and operational-safety specialist.

Add a performance/architecture specialist when measurements or product shape justify it. Do not let reconnaissance agents edit. Give them the raw repository, user contract, audit run, exact scope, and evidence format—not the parent's preferred conclusion. Use the full prompts in `references/specialist-contracts.md`.

Require each finding to name a path/symbol or journey, reproduction, observed versus expected result, user/security impact, confidence, smallest credible repair, and regression evidence. Scanner output without reachability analysis is not a vulnerability verdict; a screenshot without interaction is not functional evidence.

If subagents are unavailable, execute the same roles serially and keep their ledgers distinct. Do not silently omit a perspective.

### 5. Reconcile and prioritize before editing

The parent merges duplicate findings, reproduces contradictions, and connects each accepted issue to a user journey or trust boundary. Prioritize:

1. exposed credentials, remote execution, authorization bypass, destructive data loss, or unsafe live actions;
2. broken, inaccessible, or misleading primary user workflow;
3. silent failure, corrupt persistence/export, partial writes, and unsafe defaults;
4. reproducible correctness, reliability, install, CI, or performance failures;
5. maintainability hotspots that materially raise the above risks;
6. documentation and repository-readiness drift;
7. evidence-backed architectural recommendations outside the accepted repair scope.

Disposition every important analyzer result. For C–F rules and status taxonomy, follow `references/evidence-and-grading.md`. Do not spend the upgrade flattening harmless generated code while a dead primary action remains.

### 6. Assign bounded remediation waves

Convert the accepted ledger into small repair bundles with one observable outcome each. Spawn domain experts for bundles that can progress independently. Assign exactly one owner per mutable file and shared contract.

Keep these parent-owned unless explicitly frozen and delegated:

- public schemas, migrations, shared domain interfaces, and persistence formats;
- primary entrypoints, global configuration, lockfiles, and cross-cutting security policy;
- acceptance ledger, canonical verifier, and integration decisions.

Run work serially when bundles share a file, test, schema, route contract, migration, entrypoint, dependency set, or unresolved decision. If overlap appears, stop one owner and sequence it. Never give multiple agents “fix everything” prompts.

Require every repair to:

- reproduce the defect or characterize existing behavior;
- make the smallest repository-native root-cause change;
- add or update a regression test or executable negative case;
- preserve unrelated behavior and user changes;
- run focused positive and negative verification;
- return changed paths, exact commands/exits, limitations, generated noise, and residual risks.

Use the remediation prompt contract in `references/specialist-contracts.md`. Security changes affecting shared interfaces run before dependent work. Performance work requires a representative reproduced bottleneck and before/after measurement; complexity or Lighthouse grades alone do not justify a rewrite.

### 7. Prove the product as a user

After focused repairs, launch through the documented user entrypoint using fresh isolated state. Exercise the primary happy path and meaningful negative path. Verify loading, success, empty, validation, and operational-error states where applicable. Check logs, browser console, network failures, persistence/reopen, import/export, clean shutdown, and that controls call real shared behavior rather than canned responses.

For web UI, use a real browser and inspect screenshots critically at narrow mobile, standard desktop, and wide layouts when responsive behavior matters. Pair screenshots with interaction and console/network/output evidence. Check clipping, overflow, occlusion, contrast, hierarchy, density, focus visibility, broken media, stale or contradictory data, discoverability, and visible fixture/live status.

Complete the primary journey by keyboard, check semantic labels and actionable errors, zoom/reflow, focus order, reduced motion where applicable, and run an automated accessibility scan when available. Critical or serious reachable accessibility failures on the primary path prevent `COMPLETE`.

Measure user-visible performance only with a declared environment, representative fixture/input, and product-relevant budget. Prefer cold launch/readiness, primary action latency, large-input behavior, bundle/payload size, memory/CPU for long tasks, and relevant web vitals. Profile before optimizing and compare before/after; one warm run or aggregate score is advisory.

### 8. Harden security and GitHub readiness

Perform a threat-boundary review proportionate to the product. Inspect secrets and logs; authentication and authorization; injection; unsafe subprocesses; path traversal and archives; uploads; deserialization; SSRF; state-changing routes; CSRF/CORS/session behavior; network binding; filesystem permissions; partial writes; denial of service; and handling of sensitive data. Verify scanner findings in reachable code and test the mitigation.

Audit dependencies against project manifests/lockfiles, not an unrelated global environment. Review lock consistency, workflow permissions and action pinning, container users/secrets, unsafe generated artifacts, and license policy where material. Do not blindly upgrade dependencies or claim a scanner proves security.

Prepare the repository for honest GitHub submission: clean intended diff, no secrets or local data, useful `.gitignore`, reproducible install/build/test/launch, CI aligned with documented commands, necessary lockfiles, clear license status, and proportionate contribution/security guidance. Do not claim platforms or integrations that were not exercised.

### 9. Freeze behavior, then update documentation

After code paths and commands stabilize, spawn a technical-writer specialist. Restrict it to README, developer docs, examples, diagrams, configuration references, release notes, and an approved issue/risk record. Make it verify commands against the final tree rather than rewrite intent.

Documentation must truthfully cover the product's purpose and intended user, prerequisites, exact install/run/test commands, first successful workflow, configuration without secrets, data/persistence/export locations, fixture versus live behavior, recovery/troubleshooting, security-relevant defaults, tested platforms, and known limitations. Remove stale “production-ready,” “secure,” feature, architecture, and cross-platform claims.

Do not create duplicate process documents. Update the repository's existing source of truth. Add a concise health/known-issues record only when unresolved risk needs a durable home.

### 10. Run independent adversarial verification

Stop implementation agents. Give fresh read-only evaluators the user contract, current tree, issue ledger, and acceptance commands without a persuasive implementation narrative. Use at least a code/security regression evaluator and an end-user/browser evaluator when capacity permits.

Tell evaluators to falsify completion: inspect the actual diff, rerun canonical and issue-specific checks, reproduce original failures, exercise the real launch and negative path, reopen exported artifacts, inspect console/network/logs, recheck trust boundaries, and challenge every accepted C–F disposition. They may reject implementer self-certification.

The parent then reads every intended changed file, reconciles evaluator results, removes only proven generated noise, assigns rework serially, and reruns affected checks on the final combined tree. A retry must change scope, evidence, decomposition, tool, prompt, or strategy. After repeated similar failure, shrink to a diagnostic reproduction instead of replaying the same approach.

### 11. Close with an honest upgrade report

Classify each acceptance row using the taxonomy in `references/evidence-and-grading.md`. Overall `COMPLETE` requires:

- the documented clean launch works in the tested environment;
- a real user can complete the primary workflow and see useful output;
- a meaningful negative path fails safely and visibly;
- promised persistence/reopen/export works and artifacts reopen or parse;
- no unexplained console error, traceback, swallowed failure, unsafe partial write, or canned success remains;
- final-tree canonical tests and relevant lint, type, build, dependency, and security checks pass;
- no unresolved reachable high/critical security issue or primary-path serious accessibility issue remains;
- every important C/D/E/F hotspot is repaired, tested, or explicitly justified with evidence;
- documentation matches observed commands and behavior;
- secrets, temporary audit data, caches, screenshots, local databases, and unrelated generated noise are absent from the intended commit;
- the parent independently verified the combined tree.

Report the outcome first, then the user journeys proven, defects fixed, exact final evidence, security/accessibility/performance results, documentation changed, tested platforms, baseline failures, and residual risk. Put evidence-backed out-of-scope architecture or stack improvements in a next-steps section with impact, reason deferred, and smallest next experiment. Do not move accepted-scope defects into “future work” to manufacture completion.

Use `BLOCKED` only for missing authority, credentials, hardware, external state, or a required user decision. Hard engineering is `REWORK`, `PARTIAL`, or `FAILED` until resolved.

## Pitfalls

- **Audit theater:** a completed collector run hides failed or skipped analyzers.
- **Grade chasing:** harmless complexity is rewritten while a user journey remains broken.
- **Screenshot theater:** a polished static screen has dead actions or console failures.
- **Happy-path theater:** no invalid input, recovery, persistence, or export is exercised.
- **Fixture laundering:** deterministic demo success is reported as live integration proof.
- **Scanner certainty:** a tool line is treated as proven exploitability or safety.
- **Accessibility by score:** automation substitutes for keyboard and semantic testing.
- **Warm-machine proof:** hidden global tools, credentials, caches, or state make launch work once.
- **Agent collision:** broad specialists edit shared contracts concurrently.
- **Documentation fiction:** docs describe intended architecture instead of observed commands.
- **Scope laundering:** release blockers are relabeled as optional next steps.
- **Self-certification:** implementer summaries replace independent final-tree evidence.

## Verification checklist

- [ ] User contract, journeys, non-goals, trust boundaries, and dirty paths are explicit.
- [ ] Baseline launch, canonical checks, audit statuses, raw logs, and skipped coverage were inspected.
- [ ] Runtime, end-user/visual, and security specialists performed independent reconnaissance.
- [ ] Accepted findings have user impact, reproduction, owner, regression evidence, and disposition.
- [ ] Every D/E/F and relevant C complexity result received semantic review.
- [ ] Repair agents had non-overlapping mutable ownership and bounded prompts.
- [ ] The real launch, primary journey, negative path, persistence/export, and shutdown ran on the final tree.
- [ ] Screenshots were inspected with browser interaction, console, network, and accessibility evidence.
- [ ] Security, dependencies, performance, CI, and GitHub readiness were checked proportionately.
- [ ] A technical writer verified final commands and removed unsupported claims.
- [ ] Fresh evaluators attempted to falsify completion after implementation stopped.
- [ ] Parent reconciliation reran evidence and reported residual risks without hiding unfinished scope.
