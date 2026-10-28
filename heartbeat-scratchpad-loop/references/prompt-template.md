# Heartbeat Scratchpad Prompt Template

Replace the bracketed fields with concrete task state. Remove unused optional fields and keep each list to the next few useful items. Use absolute timestamps with a timezone, such as `YYYY-MM-DDTHH:mm:ssZ`. Store evidence pointers and conclusions rather than raw source material.

Before creating a loop, inspect existing automations for the same objective. Reuse the canonical owner when one exists. Configure cadence, timezone, and supported execution mode through the runtime's scheduling fields; state the actual cadence in the user-facing setup response. Do not promise thread continuation or an interval the runtime cannot support.

After successful creation, record the returned automation ID in the prompt using the supported update operation. Preserve the current schedule, triggers, and execution context during this and later prompt rewrites. Keep credentials and sensitive raw data out of the scratchpad.

```markdown
# Current objective
- Objective: [One concrete outcome and its success criteria.]
- Canonical automation ID: [Verified ID; populate after creation.]
- Execution context: [Verified thread or workspace reference.]

# Sources to use
1. [Tool/source and exact query, path, URL, or record identifier.]
2. [Secondary source used to validate the leading candidate.]
- Ranking criteria: [Ordered criteria and minimum evidence required.]

# Current state
- Updated: [Absolute timestamp with timezone.]
- Status: [Active, blocked, or complete, with one-line reason.]
- Last completed step: [Action and observed result; none for a new loop.]
- Signals / evidence: [Highest-signal conclusion, source pointer, checked-at timestamp.]
- Last notification: [Timestamp and event/candidate already reported, or none.]
- Consecutive failed or no-progress wakes: [Count and cause.]
- Git checkpoint, if applicable: [Repo path, branch, last verified commit, and commit policy.]

# Ranked candidates / hypotheses / tasks
1. [Candidate] — [Evidence, rank rationale, uncertainty, next validation.]
2. [Candidate] — [Evidence, rank rationale, uncertainty, next validation.]
3. [Candidate] — [Evidence, rank rationale, uncertainty, next validation.]

# Deprioritized items
- [Item] — [Reason; revisit only if a specific signal changes.]

# Next actions
1. [Smallest concrete step for the next wakeup.]
2. [Follow-up if the first step succeeds.]
3. [Fallback if the evidence contradicts the leading candidate.]

# Progress and notifications
- Progress means: [A validated item, resolved uncertainty, or durable completed step.]
- Notify when: [Specific change, confidence level, result, or blocker worth reporting.]
- Deduplicate against: [Last notification and completed-step state above.]

# Guardrails
- Perform one focused unit of work per wakeup; validate or rank 1-3 concrete items.
- Preserve the objective, authorized scope, ranking criteria, notification threshold, and stop condition unless the user changes them.
- Authorized actions: [Concrete permitted actions and boundaries.]
- Check source timestamps and distinguish observed evidence from hypotheses.
- Recheck completed-step and git state before repeating an action after interruption.
- If applicable, commit each meaningful durable step in the named project repo; stage only task changes and follow the user's push authorization.
- Rewrite compact state in this automation's prompt; retain its ID and current scheduling/trigger configuration.
- If state cannot be read or saved, report the blocker without claiming persistence or creating a duplicate loop.

# Stop condition
- Success: [Measurable completion condition.]
- Expiry or staleness: [Absolute deadline or concrete condition.]
- Retry/no-progress limit: [Bound selected for this task.]
- On stopping: preserve the final result and reason, then delete this automation or disable it when deletion is unavailable; verify success and report the outcome.

# Each wakeup
1. Read this automation's current prompt and configuration. Stop immediately if a terminal condition already applies.
2. Inspect the relevant sources and perform the first focused next action.
3. Checkpoint meaningful durable work to git when applicable.
4. Replace stale state, rerank the shortlist, prune obsolete items, and persist the complete compact prompt to the same automation. Preserve objective and guardrails.
5. Notify only when the threshold is crossed or the loop ends. Record the notification result in state to avoid repeated alerts.
6. If a stop condition is now met, delete or disable the automation and verify that future wakeups have stopped.
```

If a tool call fails, retain the last verified result, record the failure and next recovery step, and count the failure toward the task's retry limit. Do not convert an unverified action into completed state. When the objective or execution shape changes, update the existing owner and its compact contract instead of leaving stale instructions active.
