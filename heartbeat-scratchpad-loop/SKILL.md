---
name: heartbeat-scratchpad-loop
description: Build or run a long-lived task as a self-modifying thread heartbeat where the automation prompt acts as compact working memory. Use when the user wants an automation, monitor, recurring check-in, polling loop, watch task, or long-running search/research/process that should wake up over time, do one focused step, rewrite its own state, and continue later.
---

# Heartbeat Scratchpad Loop

Use this skill when the user wants a lightweight long-running task that persists through thread heartbeats and updates itself over time.

The core pattern is:

- the thread is the execution surface
- the available tools are the action surface
- the automation prompt is the scratchpad

Prefer this over a static reminder when the task needs memory, iteration, ranking, reprioritization, or recurring validation.

## When To Use

Use this skill for requests like:

- "set up a loop to keep checking this"
- "poll yourself every few minutes and keep going"
- "monitor this topic/contact/project over time"
- "create a long-running search task"
- "use automations as a scratchpad"
- "wake this thread later and continue"

Do not use this pattern for:

- one-shot reminders with no state
- tasks that should obviously be a detached cron job against a workspace instead of a thread
- tasks with no clear objective or no meaningful action surface

## Workflow

### 1. Decide the execution shape

- Prefer a `heartbeat` automation when the task should continue in the current thread.
- Prefer `cron` only when the work should run detached against a workspace.
- If an existing automation already owns the task, update it instead of creating a duplicate.
- Verify the active runtime supports the intended execution shape and cadence; follow the compatibility guidance under **Tooling**.

### 2. Reduce the task to objective X plus tool/data surface Y

Define, in plain terms:

- objective
- data sources and tools
- ranking criteria
- what counts as progress
- notification threshold
- stop condition
- cadence

### 3. Seed the first prompt compactly

The first prompt should contain:

- `Current objective`
- `Sources to use`
- `Current state`
- `Ranked candidates / hypotheses / tasks`
- `Deprioritized items`
- `Next actions`
- `Guardrails`
- `Stop condition`

Read [references/prompt-template.md](references/prompt-template.md) when you need a scaffold. Record the canonical automation ID once creation succeeds, and retain it across rewrites.

### 4. Run the control loop on each wakeup

Each heartbeat should do one focused unit of work:

- inspect the current automation state and check whether the stop condition has already been met
- inspect the external sources
- validate or rank 1-3 concrete items
- checkpoint durable work to git when the project is in a git repo and a meaningful unit of progress has landed
- rewrite the automation prompt with fresher compact state
- notify the user only if something crosses the notification threshold

Do not let the loop sprawl. Small focused steps beat broad rescans. Record the last completed action, evidence timestamps, and last notification so retries do not repeat completed work or alerts. If reading or persisting the automation state fails, report the blocker without creating a replacement loop or claiming the checkpoint succeeded.

### 5. Keep the scratchpad compact

- Overwrite stale sections instead of appending endlessly.
- Promote only the highest-signal facts into the prompt.
- Keep lists ranked.
- Use absolute dates.
- Remove obsolete branches.
- Preserve the user's objective, authorized scope, notification threshold, and stop condition while updating evidence, rankings, and next actions.

### 6. Close the loop when done

- Delete the automation when the objective is complete, stale, or no longer worth polling; disable it if the runtime does not expose deletion.
- If the task survives but the shape has changed, update the automation instead of letting stale instructions linger.
- Verify the terminal action succeeded before reporting that polling has stopped.

## Version Control

When the control loop is working inside a project repo:

- make small checkpoint commits as meaningful units of work land
- prefer one commit per durable step rather than one giant catch-up commit
- keep commit messages concrete and stateful
- if no git repo exists for a project that clearly needs ongoing checkpointing, initialize one at the project root unless the user has said not to
- mention the repo path and commit behavior when seeding or updating the loop prompt so the automation keeps treating commits as part of progress
- stage only the task's changes, preserve unrelated work, and follow the user's authorization for pushes or other external actions

## Scratchpad Rules

- The prompt is short-term memory, not a transcript.
- Prefer ranked bullets over narrative paragraphs.
- Store conclusions, not raw dumps.
- Track only the next few actions, not every possible branch.
- Keep one automation as the canonical owner for one subproblem.

Good scratchpad sections:

- `Current objective`
- `Signals / evidence`
- `Ranked leads`
- `Open questions`
- `Next actions`
- `Guardrails`

## Multi-Automation Pattern

For bigger tasks, split by role:

- `scout`: finds new candidates
- `validator`: checks whether candidates are real/relevant
- `monitor`: watches inbox/calendar/messages/news/source changes
- `coordinator`: maintains the merged shortlist and user-facing updates

Only split when the loops are genuinely separable. If not, keep one automation. Give each loop a distinct subproblem and canonical ID; make the coordinator responsible for merged rankings and user-facing updates.

## Tooling

Use `automation_update` to create, update, view, or delete the automation when that interface is available. Otherwise, inspect the active automation tools and map those operations to their supported APIs. A runtime may expose separate create, peek/list, and update operations, with disabling available instead of deletion.

Preserve the canonical automation ID, schedule, execution context, and triggers while rewriting the prompt. Read the current configuration first; if the API requires the complete webhook trigger set on update, carry it forward unchanged.

Verify support for thread continuation, execution modes, and cadence before scheduling. Do not assume `heartbeat`, `cron`, or sub-hour intervals are supported, and do not simulate unsupported cadence with duplicate automations or busy waiting. If the runtime cannot persist prompt updates or continue in the required context, explain that limitation and retain the prepared scratchpad without claiming the loop is active. Confirm creation or update from the tool result before reporting success.

## Response Style

When building one of these loops:

- say what the loop is for
- say what tool/data surfaces it will use
- make the automation prompt the scratchpad
- keep cadence and stop conditions explicit
- prefer concrete ranked state over vague ambitions
