---
name: goosnav-parent-verification
description: Reconcile delegated coding-agent work against the repository and the original contract by inspecting diffs, rerunning canonical and project-specific verifiers, browser-smoking user interfaces, cleaning generated noise, and classifying complete, partial, blocked, or failed work honestly. Use after subagents, parallel agents, long autonomous runs, or inherited implementation claims.
version: 1.0.0
author: Goosnav LLC
license: Proprietary; internal use permitted
metadata:
  hermes:
    tags:
      - verification
      - agent-review
      - browser-smoke
      - diff-reconciliation
      - evidence
    related_skills:
      - goosnav-mvp-delivery
      - goosnav-agentic-orchestration
      - goosnav-software-productization
---

# Overview

The parent agent owns the delivered result. Delegation transfers implementation effort, not responsibility for correctness, scope, safety, or truthful reporting. Verify the repository as it exists now; agent summaries are leads, never evidence.

Reconciliation answers four separate questions:

```text
Was the requested scope changed intentionally?
Does the diff implement that scope without collateral damage?
Do the strongest relevant checks pass in the current tree?
Can a user complete the visible workflow?
```

A green unit suite may coexist with a dead button. A polished browser screen may hide a broken export. A child may have tested an earlier tree while another agent changed the same files. Parent verification closes those gaps and produces a status that another person can trust.

## When to Use

Use after coding agents or subagents report completion, after multiple branches or patches are combined, when inheriting an autonomous run, before a release/commit, or whenever a “done” claim is not backed by reproducible evidence. It also applies to rescue work where generated files, debug state, and partially overlapping changes obscure the intended patch.

Do not use this as a substitute for normal implementation tests after every small edit. It is the independent convergence pass. If the repository has not been changed and the user only wants a design review, inspect without mutating or cleaning.

## Workflow

1. **Freeze the acceptance contract.** Restate the original requested outcomes, prohibited actions, file boundary, required checks, owner-gated actions, and expected artifact. Incorporate explicit later amendments. Do not let a child’s summary redefine the request. Create a compact ledger with `required`, `evidence`, and `status` columns.

2. **Capture repository state before cleanup.** Run status, branch, recent commit, and diff summaries. Include staged, unstaged, and untracked files. Preserve unrelated user changes. If the worktree was already dirty, distinguish baseline paths from delegated paths using available preflight notes, timestamps only as hints, and semantic diff inspection.

3. **Inventory agent claims.** For each delegated task, record claimed files, commands, results, limitations, and handoff artifacts. Mark claims with no command output or observable artifact as `UNVERIFIED`. If parallel agents touched the same contract or file, flag a reconciliation hotspot.

4. **Inspect the actual diff semantically.** Read every intended changed file and enough surrounding code to understand dependency direction. Check for scope expansion, deleted behavior, duplicated cores, hard-coded fixture success, swallowed errors, unsafe filesystem/network actions, secrets, dependency additions, and documentation drift. Review binary/generated additions by provenance and necessity, not just size.

5. **Run fast structural checks.** Use repository-native formatting, lint, type, schema, and unit commands. Run them from the documented working directory with the documented runtime. Record exact commands and exit codes. If a command is unavailable, distinguish missing tooling from code failure; do not rewrite the toolchain during verification unless asked to fix.

6. **Rerun canonical verifiers.** Prefer the project’s single verifier, then run focused checks required by the changed boundaries. A child’s past pass is stale when the tree changed afterward. Avoid selectively skipping a known failure. If the canonical verifier is destructive, costly, or requires external authority, run safe subchecks and classify the remainder explicitly.

7. **Exercise the integrated runtime.** Start the application from its user-facing entrypoint with isolated state. Confirm readiness, logs, primary workflow, persistence/export, expected failure, and clean shutdown. Use deterministic fixtures where live services are not authorized. Verify fixture labels and never report fixture success as live integration success.

8. **Browser-smoke every changed UI workflow.** Use a real browser engine or approved browser-control tool. Check initial render, navigation, primary actions, input validation, loading, success, empty/error state, refresh/reopen, viewport/overflow, console errors, and relevant network responses. Inspect screenshots visually when layout matters. API calls alone do not prove UI operability.

9. **Test changed interfaces at their seams.** When GUI, CLI, API, persistence, provider, or export contracts changed, run parity or contract checks. Compare shared inputs and normalized results. Validate exported artifacts by reopening or parsing them, not merely checking that a file exists.

10. **Clean generated noise cautiously.** Remove only files proven to be transient products of this verification or delegated work: caches, bytecode, logs, temporary databases, browser profiles, test screenshots, build outputs, and copied fixture exports. Respect tracked fixtures and user artifacts. Use targeted removal, never broad destructive reset commands. Recheck status after cleanup.

11. **Classify each acceptance item.** Use the status taxonomy below. One blocker does not erase working slices, but it prevents an overall `COMPLETE` claim. A failure outside scope is still reported if it affects confidence or the repository baseline.

12. **Fix only when authorized.** If the user asked to implement and finish, correct small in-scope defects and rerun affected evidence. If asked only to review or diagnose, report findings without expanding into a repair. Preserve a tight distinction between verification changes (such as deleting generated noise) and product fixes.

13. **Produce the reconciliation report.** Lead with overall classification. List acceptance items, actual diff, commands/results, browser observations, cleaned paths, remaining work, blocked external dependencies, and unsupported claims. State whether a commit/release is safe. Do not hide baseline failures.

## Status Taxonomy

- `COMPLETE`: every required item has current observed evidence; no material known defect remains.
- `PARTIAL`: a useful coherent subset works, but one or more requested items lack implementation or evidence.
- `BLOCKED`: completion requires missing authority, credentials, hardware/platform, external state, or a user decision; all safe local work is exhausted.
- `FAILED`: implemented behavior contradicts the contract, corrupts state, creates unacceptable risk, or cannot pass essential checks.
- `BASELINE_FAILURE`: a reproducible pre-existing problem outside the delegated diff. It does not automatically condemn the patch, but it limits the overall assurance.
- `UNVERIFIED`: a claim has not been exercised. It is not a softer synonym for pass.

Use `BLOCKED` narrowly. A hard bug is usually `FAILED` or `PARTIAL`, not blocked. Missing optional tooling may leave only that check `UNVERIFIED` while other evidence stands.

## Evidence Discipline

Good evidence contains the exact command/action, current commit or tree state, exit/result, and the boundary it proves. Examples:

- `python3 scripts/verify.py` exited 0 and reported 42 tests plus one browser smoke;
- export `result.schema-v1.json` parsed and reopened with three records;
- manual browser smoke at a named route completed create-edit-export, with no console errors;
- Windows launcher was not executed because no Windows environment was available.

Bad evidence includes “looks correct,” “the child said it passed,” a screenshot of a static page with no action, compilation presented as runtime support, or a test command from before the final merge.

## Pitfalls

- **Summary anchoring:** trusting the implementation narrative and reading only named files. Start from status and diff.
- **Green-test tunnel vision:** stopping at unit tests while the user entrypoint fails. Run the integrated workflow.
- **Concurrent stale evidence:** accepting tests run before another agent’s overlapping changes. Rerun on the final tree.
- **Cleanup overreach:** deleting an untracked user artifact or resetting unrelated edits. Prove provenance and remove narrowly.
- **Browser theater:** opening the page but not interacting, watching the console, or validating output.
- **Blocked inflation:** calling normal unfinished engineering “blocked.” Reserve it for missing authority or external capability.
- **Silent baseline:** omitting pre-existing failures because they were not caused by the patch. Separate causation from release confidence.
- **Fixing during review:** changing behavior without authorization and muddying the evidence. Respect the request type.

## Verification Checklist

- [ ] Original acceptance criteria and later amendments are captured.
- [ ] Staged, unstaged, and untracked changes were inventoried before cleanup.
- [ ] Every intended changed file received semantic review.
- [ ] Agent claims are mapped to current evidence or marked unverified.
- [ ] Canonical and boundary-specific checks ran on the final tree.
- [ ] The actual user launch path and clean shutdown were exercised.
- [ ] Changed UI workflows received an interactive browser smoke and console check.
- [ ] Persistence/export artifacts were reopened or parsed.
- [ ] Fixture evidence is visibly distinct from live evidence.
- [ ] Only proven generated noise was removed; unrelated changes remain.
- [ ] Baseline failures and untested platforms are explicit.
- [ ] Overall status uses `COMPLETE`, `PARTIAL`, `BLOCKED`, or `FAILED` honestly.

## Exact Recipe

Recipe: reconcile three agents that changed a local browser analytics tool.

1. Restate required outcomes: import CSV, edit field mapping, render summary, export JSON, launch locally, and keep an unrelated user-edited sample file untouched.
2. Capture `git status --short`, `git diff --stat`, staged diff, and untracked paths. Note that agents claimed backend, UI, and tests respectively.
3. Read the import service, API route, UI form/handlers, export serializer, verifier, and docs. Discover whether the UI calls the new route and whether both exports use the shared schema.
4. Run the canonical verifier on the combined tree. Then start with a temporary data directory and import a deterministic invented CSV.
5. In a real browser, change a mapping, submit, inspect the network response and console, refresh, reopen the saved project, export JSON, and parse it. Trigger an invalid-column error and verify no partial project was written.
6. Remove only the browser profile, temporary database, test export, and bytecode created by the run. Recheck status and confirm the user sample remains modified and unstaged.
7. Classify: backend/import and persistence `COMPLETE`; UI mapping `PARTIAL` if refresh loses one label; live cloud ingestion `UNVERIFIED` and out of scope. Overall requested work is `PARTIAL`, safe to continue but not release.
8. If implementation authority includes fixes, correct the refresh defect, rerun verifier and browser steps, then change overall status to `COMPLETE` only when current evidence passes.
