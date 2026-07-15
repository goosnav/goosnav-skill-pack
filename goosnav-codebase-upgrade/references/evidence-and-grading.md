# Evidence, grading, and completion rules

## Evidence levels

- `OBSERVED`: exact current-tree command or user action, working directory/environment, exit/result, and relevant artifact/log are recorded.
- `INFERRED`: source or symptoms support a conclusion, but the behavior has not been reproduced. State the reasoning and confidence.
- `CLAIMED`: a person, agent, comment, README, or prior report says it works. Use only as a lead.
- `UNVERIFIED`: the boundary was not exercised or usable evidence is missing. This is never a soft pass.

Evidence goes stale after overlapping edits. Rerun it on the final combined tree. A unit test proves its assertion, not the launch path, browser control, live provider, or user value.

## Audit status interpretation

- `PASS`: the named command exited successfully in the recorded environment. Inspect scope and configuration before generalizing.
- `FINDINGS`: an analyzer reported candidate issues. Perform semantic review, reachability analysis, and false-positive disposition.
- `FAIL`: a test or required check contradicted its contract. Reproduce and fix or classify honestly.
- `ERROR`: the command, configuration, environment, or collector failed. The intended boundary remains unverified.
- `SKIPPED`: the check did not run. Record the reason and use a proportionate alternative or leave the boundary unverified.
- `NOT_APPLICABLE`: use only after inspecting the product boundary and explaining why the check cannot apply.

Never average these statuses into a reassuring score. One reachable high-impact defect can dominate dozens of passes.

## Complexity grades

Radon cyclomatic-complexity bands are generally:

| Grade | Complexity | Required handling |
| --- | ---: | --- |
| A | 1–5 | Normal review; not proof of correctness. |
| B | 6–10 | Review with surrounding tests. |
| C | 11–20 | Inspect when primary-path, trust/data/money boundary, high-churn, or weakly tested. |
| D | 21–30 | Create a disposition row and inspect semantically. |
| E | 31–40 | Treat as a high-priority maintainability/testability risk unless proven isolated. |
| F | 41+ | Treat as an urgent characterization and repair candidate, especially when reachable. |

Radon Maintainability Index uses a separate A/B/C scale. Do not conflate MI C with cyclomatic C or invent D–F MI grades.

A grade is not a bug. Before refactoring, record reachability, user/security impact, churn, coverage, branching behavior, and whether generated code, a parser, or a state machine justifies the shape. Characterize behavior first. Refactor only when it removes observed risk or makes important behavior testable. A low-graded but broken action outranks a high-complexity harmless helper.

## Severity and issue status

Prioritize by user harm, exploitability, affected assets, likelihood, blast radius, recoverability, and primary-workflow criticality.

- `ACCEPTED`: current independent evidence satisfies the item.
- `REWORK`: the repair exists but does not satisfy the item or caused a regression.
- `PARTIAL`: a useful coherent subset works, but accepted scope remains unfinished or unverified.
- `FAILED`: behavior contradicts the contract, creates unacceptable risk, corrupts data, or essential checks fail.
- `BLOCKED`: completion requires missing authority, credential, hardware, external state, or a user decision after safe local work is exhausted.
- `BASELINE_FAILURE`: a reproduced pre-existing problem outside the change; it still limits release confidence.
- `UNVERIFIED`: no current evidence. It cannot support `COMPLETE`.

Hard or time-consuming engineering is not blocked. Do not relabel accepted-scope failure as a future enhancement.

## User and screenshot evidence

Freeze three to seven user journeys with expected visible results and failure/recovery behavior. Execute through the documented entrypoint with fresh state. Pair each screenshot with the interaction, console/network/log evidence, and persisted or exported result it is meant to show.

Inspect meaningful initial, loading, success, empty, validation-error, and operational-error states where applicable. At representative narrow, desktop, and wide viewports check:

- clipped, overflowing, occluded, or unreachable content;
- illegible text, contrast, hierarchy, density, alignment, and broken media;
- primary-action discoverability and honest loading/disabled feedback;
- stale, contradictory, truncated, fixture, or live data labeling;
- keyboard reachability, focus order/visibility, semantic names, actionable errors, zoom/reflow, and reduced motion.

A screenshot proves appearance at one instant. It does not prove the button works, the request succeeded, the result persisted, or the export reopens.

## Security and supply-chain evidence

Start from trust and data boundaries. Verify secrets, authn/authz, injection, subprocess and filesystem use, traversal/archive handling, uploads, deserialization, SSRF, network binds, state-changing web routes, CSRF/CORS/session defaults, permissions, logs, partial writes, resource exhaustion, and sensitive-data handling as applicable.

Scanner output is a hypothesis. Establish configuration, reachable source-to-sink path, real dependency/lockfile scope, exploit/failure consequence, and a regression test. A clean scan is not a security guarantee. Missing advisories because a network or database was unavailable remain unverified and timestamped.

## Performance evidence

Declare product-relevant budgets before optimizing. Measure a representative input and production-shaped or clean environment, with cold and repeated runs where useful. Record environment and variance. Prefer user-visible readiness/latency, large-input behavior, web vitals, query counts, payload/bundle size, and sustained CPU/memory. Profile before rewriting. Compare before/after against the same fixture; do not market one aggregate score as proof.

## Documentation and GitHub truth gate

Copy-paste documentation commands from the stated directory against the final tree. Verify prerequisites, install, launch, primary workflow, configuration, data/export locations, tests, recovery, security defaults, fixture/live status, limitations, and supported-platform claims.

Before calling a repository GitHub-ready, inspect intended status/diff, ignore rules, credentials/local data, generated artifacts, lockfiles, CI parity, workflow permissions/action pinning, license status, useful repository metadata, and clean-checkout or archive build when feasible. Do not add ceremonial files the project does not need; do not omit material legal/security ambiguity.

## Completion proof

The parent may call the upgrade `COMPLETE` only from current final-tree evidence. Report commands and user actions, not adjectives. Separate tested from untested platforms and fixture from live integrations. List residual risks and out-of-scope architectural next steps with evidence, impact, why deferred, and the smallest next experiment.
