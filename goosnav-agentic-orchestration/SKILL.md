---
name: goosnav-agentic-orchestration
description: Coordinate Claude, Codex, and local models through capability-aware allocation, repository preflight, narrow prompts, explicit serial/parallel rules, durable recovery handoffs, evaluator contracts, and anti-repeat strategy updates. Use for multi-agent software work where independent tasks can accelerate delivery without losing ownership, evidence, or context.
version: 1.0.0
author: Goosnav LLC
license: Proprietary; internal use permitted
metadata:
  hermes:
    tags:
      - multi-agent
      - orchestration
      - model-allocation
      - recovery
      - evaluation
    related_skills:
      - goosnav-parent-verification
      - goosnav-mvp-delivery
      - goosnav-research-simulation
---

# Overview

Use multiple models only when their independence creates real leverage. The orchestrator owns scope, dependency ordering, shared state, cost, authority, final integration, and truthfulness. Workers receive bounded problems and return evidence-bearing handoffs; evaluators judge explicit contracts rather than style.

The control loop is:

```text
preflight -> decompose -> allocate -> execute -> reconcile -> evaluate
                   ^                                  |
                   +------ strategy update <----------+
```

Parallelism is a resource, not a default. Two agents editing the same contract usually create reconciliation debt. One agent with sufficient context is often faster. Spawn or invoke another model only for a concrete, bounded subtask that can progress independently while useful work continues.

## When to Use

Use when a project explicitly calls for delegation, has multiple separable components, needs independent implementation and evaluation, benefits from a cheap local model for repetitive bounded work, or must recover across interrupted contexts. It also fits model-routing systems and founder workflows that coordinate several coding assistants.

Do not use it to simulate a team for a one-file change, to evade a tool/permission boundary, or to keep retrying the same failed prompt. If delegation is not authorized by the environment or user, apply the preflight and evaluator ideas within one agent rather than spawning.

## Workflow

1. **Establish orchestration authority.** Confirm which agents/models and tools may be used, concurrency limits, file boundaries, network/external-action rules, budget/latency constraints, and who may commit, send, publish, or deploy. Agent availability is not authorization for external actions.

2. **Run repository and objective preflight.** Inspect instructions, current branch/status, dirty files, build manifests, canonical checks, architecture boundaries, and active acceptance contract. Record a baseline command when feasible. Identify user-owned changes that workers must preserve.

3. **Build the dependency graph.** Break the goal into output contracts, not job titles. For each task name inputs, allowed paths, prerequisites, produced artifact/diff, verifier, failure modes, and downstream consumers. A task is parallel-ready only if it does not need a pending decision or mutate an overlapping contract.

4. **Allocate by capability and cost.** Use the strongest model for ambiguous architecture, security boundaries, cross-file integration, and final reconciliation. Use capable coding models for well-scoped implementation. Use cheaper/local models for deterministic transformations, test-case enumeration, log classification, or first-pass inventory when their output is independently checked. Never send secrets or sensitive data to a model/provider without authorization.

5. **Choose serial versus parallel explicitly.** Run serially when tasks share files, schemas, migrations, public API, acceptance decisions, or a scarce live environment. Parallelize read-only research or implementation slices with stable non-overlapping contracts. Assign one owner per mutable contract. If overlap becomes apparent, pause one task and sequence it.

6. **Write narrow worker prompts.** Include objective, relevant context, allowed/forbidden paths, concrete deliverable, tests to run, non-goals, expected handoff format, and instruction to preserve unrelated changes. Avoid “fix everything” or pasting irrelevant history. Ask the worker to inspect before editing and to report blockers without inventing completion.

7. **Define an evaluator contract before execution.** State acceptance checks observable from the final tree: required behavior, invariant, command, artifact, negative case, and status taxonomy. Separate worker self-checks from parent/evaluator checks. The evaluator must be allowed to reject a persuasive implementation summary.

8. **Launch within the safe concurrency envelope.** Keep at least one coordination slot available when the platform requires it. Track task state as `PENDING`, `RUNNING`, `HANDOFF_READY`, `RECONCILING`, `ACCEPTED`, `REWORK`, or `BLOCKED`. Do not create duplicate tasks simply because a worker is slow; first inspect status or wait.

9. **Collect durable handoffs.** Require changed paths, decisions, exact commands/results, limitations, unresolved questions, generated noise, and next integration step. For long tasks, checkpoint semantic state in a repository-approved handoff or message: what is true now, not a transcript of every action.

10. **Reconcile before trusting.** Inspect the actual diff and current status. Resolve overlapping assumptions, schema drift, duplicate abstractions, and stale tests. Rerun the integrated verifier after all relevant work lands. Use Parent Verification for the full convergence pass, including browser smoke when UI changed.

11. **Recover by changing information or strategy.** When a worker fails, classify cause: missing context, ambiguous contract, tool/environment, code defect, capacity, or model limitation. A retry must change at least one of context, scope, decomposition, model, tool, example, or acceptance test. Do not replay the same prompt unchanged.

12. **Create a recovery handoff.** Give the successor current tree state, task contract, attempted commands, exact failure, retained useful changes, rejected approaches, and the smallest next experiment. Do not make it rediscover the entire repository. Stop concurrent edits to the same paths during recovery.

13. **Evaluate independently.** Run contract checks and inspect evidence on the final combined state. Classify each task `ACCEPTED`, `REWORK`, `PARTIAL`, `BLOCKED`, or `FAILED`. Worker success plus integration failure means the overall item is not accepted.

14. **Update the anti-repeat ledger.** Record failure signature, likely cause, strategy attempted, observed result, and next allowed strategy. Before retrying, compare the new plan. After two similar failures, shrink the slice and run a diagnostic experiment; after three, escalate the decision or mark genuine external blockage according to the operating rules.

15. **Close workers and report the parent outcome.** Ensure no unnecessary agent remains mutating state. Report accepted outputs, final verification, rejected/partial work, model limitations, owner-gated next actions, and repository status. The orchestrator—not the workers—makes the completion claim.

## Allocation Heuristics

Choose models using task risk rather than brand loyalty:

| Task shape | Allocation |
| --- | --- |
| Ambiguous architecture or security boundary | strongest reasoning model, serial |
| Focused implementation with stable tests | coding model, potentially parallel by non-overlapping path |
| UI implementation plus visual judgment | frontend-capable model, then independent browser evaluator |
| Mechanical inventory/classification | cheap or local model, output checked by parent |
| Final diff, integration, release claim | parent/strong evaluator, serial |
| Sensitive source or credentials | only authorized local/provider boundary; otherwise redact or do not delegate |

Cost optimization never weakens the evaluator contract. A cheap worker is useful when a false output is easy to detect, not when an undetected mistake is expensive.

## Worker Contract Template

```text
Objective: <one observable outcome>
Allowed paths: <exact paths>
Read first: <instructions/contracts>
Preserve: <dirty/user-owned paths>
Non-goals: <explicit exclusions>
Deliver: <diff/artifact/schema>
Verify: <exact commands and negative case>
Handoff: changed paths; decisions; commands/results; limitations; noise
Stop/escalate if: <authority, overlap, ambiguity, destructive action>
```

## Evaluator Contract Template

```text
Acceptance item | observable evidence | command/action | pass rule
Invariant       | inspected boundary  | test/review    | no violation
Integration     | final combined tree | canonical run  | current pass
Classification  | complete/partial/blocked/failed with reason
```

Evaluation prompts should identify the contract and repository state but avoid telling the evaluator that the worker “did a great job.” Reduce anchoring.

## Pitfalls

- **Agent theater:** delegation adds messages but no independent throughput.
- **Shared-file parallelism:** workers race on one schema or entrypoint and invalidate tests.
- **Model mysticism:** allocation uses reputation instead of task/evaluation risk.
- **Prompt dumping:** workers receive huge context without a bounded output contract.
- **Self-certification:** worker tests are treated as independent acceptance.
- **Retry loops:** the same prompt, context, and model repeat the same failure.
- **Transcript handoffs:** thousands of tokens obscure the exact current state and next experiment.
- **Authority diffusion:** a worker sends, publishes, deletes, or commits because the tool was available.
- **Orphan workers:** background tasks keep changing files after reconciliation begins.
- **Partial erasure:** useful completed slices disappear behind a single broad “failed” label.

## Verification Checklist

- [ ] Delegation authority, concurrency, file, data, cost, and external-action boundaries are explicit.
- [ ] Baseline repository state and canonical checks were captured.
- [ ] Every task has inputs, allowed paths, output contract, verifier, and owner.
- [ ] Parallel tasks do not overlap mutable contracts or pending decisions.
- [ ] Model allocation matches ambiguity, sensitivity, and detection cost.
- [ ] Worker prompts include non-goals, preservation rules, and handoff format.
- [ ] Evaluator contracts existed before implementation claims.
- [ ] Handoffs contain paths, decisions, exact results, limitations, and noise.
- [ ] Final diff and verifier were reconciled on the combined tree.
- [ ] Every retry changed strategy and updated the anti-repeat ledger.
- [ ] Recovery handoffs preserve useful work and name the next experiment.
- [ ] Overall completion is asserted by the parent from independent evidence.

## Exact Recipe

Recipe: coordinate a backend slice, UI slice, and independent verifier for a local workbench.

1. Preflight finds a dirty user-edited fixture, one shared API schema, and a four-slot concurrency limit. Preserve the fixture and make the parent own the schema.
2. Serially define the application-service and API request/response contract. Run its contract tests before delegation.
3. Assign worker A only the persistence adapter and migration paths; assign worker B only UI components consuming the frozen schema; assign worker C a read-only test-gap inventory and browser-smoke plan. Give each exact allowed paths and handoff fields.
4. Allocate strong coding models to A/B and a cheap local model to C because its inventory will be checked. Do not let C edit files. Continue parent work on integration fixtures while A/B run.
5. Reconcile handoffs and actual diffs. If B assumed a different error code, update B serially after A stops rather than having both edit the schema.
6. Run the combined canonical verifier and interactive browser create-edit-export-reopen flow. The parent checks the dirty user fixture remains untouched.
7. If export fails twice with the same timeout, log the signature and replace the third broad retry with a small service-level timeout reproduction. Hand the reproduction and current diff to one successor model.
8. Accept only when the combined tree passes contract, migration, browser, artifact reopen, and cleanup checks. Report model C’s inventory as advisory input, not proof.
