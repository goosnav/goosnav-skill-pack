---
name: goosnav-modular-coding-method
description: Build software one testable black-box module at a time -- contract before code, testbench before implementation, one brick per turn, human sign-off between bricks, and a growing assembly proven at every rung -- instead of one sprawling pass that lands eighty percent done and impossible to debug. Use when writing new code, planning a system's module map, or carving modules out of an existing codebase, and whenever the request sounds like "build it step by step", "module by module", "one piece at a time", "don't build the whole thing at once", "keep it small and testable", or "I need to be able to understand and tweak this myself".
---

# Goosnav Modular Coding Method

An agent-built system arrives about eighty percent right. The last twenty percent is the human's, and it is where the product actually lives. A system generated in one pass makes that twenty percent unreachable: nothing is legible, no boundary is trustworthy, and every fix perturbs code nobody has read. The defect is not model quality. It is granularity.

So build the house brick by brick. One module, contracted as a black box, tested until it is boring, accepted by a human, then joined to the assembly and the seam tested too. Two bricks, then three. This skill is the build loop, and it constrains you: your default unit of work is **exactly one brick**, after which you stop.

## Core rules

- Build one brick per turn. Write it, prove it, report it, then stop. Do not start the next brick.
- Contract before code. Testbench before implementation. No exceptions, including for "obvious" modules.
- Every brick is a black box with known inputs, known outputs, and a contract written in its own file header.
- Every brick declares `CORE` (pure) or `SHELL` (adapter). Business logic in a `SHELL` brick and I/O in a `CORE` brick are both violations.
- Every brick is runnable alone: a sibling testbench that gates it, and a demo entry point a human can watch produce real output.
- The header carries what and why. Inline comments carry why only. Restating code in English is banned.
- Never modify an `ACCEPTED` brick without a contract change issued by the human.
- Never build ahead. No scaffolding directories, no stubs for unbuilt bricks, no `TODO` placeholders, no framework setup before a brick needs it.
- Only a human moves a brick to `ACCEPTED`. Passing tests are evidence, not acceptance.

Read [references/module-contract.md](references/module-contract.md) before writing any brick. Read [references/testbench.md](references/testbench.md) before writing any test. Load the recipe for the project's language from the map at the end of this file.

## When not to use this

Use `nasa-v-model` when the deliverable is a traceable specification suite before anyone codes; this skill starts where that one ends and will consume its architecture as a module map. Use `goosnav-codebase-upgrade` when an existing product needs an adversarial audit and repair rather than new modules. Use `goosnav-software-productization` when working code needs packaging and distribution. This skill owns the act of writing code, and nothing else.

Do not use it for a throwaway script, a one-line fix, or an exploratory spike you intend to delete. Ceremony costs more than the artifact is worth. Say so and write the script.

## The brick

One brick is one module in one file: a single public entry point (three public symbols maximum), a written contract, a sibling testbench, and a demo. It is defined by its interface, not its implementation -- a caller may depend on the contract and nothing else.

Every brick file opens with this header, in the language's comment or docstring syntax:

```text
PURPOSE    One sentence. What this black box does.
KIND       CORE | SHELL
CONTRACT   IN:  <name: type> -- precondition
           OUT: <type> -- postcondition
           RAISES: <error> when <condition>
GUARANTEES Invariants. What this brick will never do.
TUNING     Named constants a human is expected to change, with range and effect.
DECISIONS  D1: chose <X>. Alternative: <Y>. Why not: <Z>. Revisit if: <trigger>.
LIMITS     Known unhandled cases, explicitly outside the contract.
TESTBENCH  <path> -- run with: <exact command>
```

`DECISIONS` is the part agents skip and humans need most. Every non-trivial choice gets a numbered entry with a real alternative and a real reason, and a trigger that tells a future reader when the decision expires. "Chose a dict for speed, alternative a list, dicts are faster" is not a decision record. If a choice had no alternative worth stating, it was not a decision -- do not pad the section.

Hard limits, all checkable:

- One public entry point; three public symbols maximum.
- Five inputs maximum before they become a named struct.
- Two hundred implementation lines soft, three hundred hard. At the hard cap, stop and re-split.
- Three dependencies maximum, every one of them already `ACCEPTED`. Zero dependencies on unbuilt bricks.

Status ladder: `PLANNED` -> `CONTRACTED` -> `RED` -> `GREEN` -> `ACCEPTED` -> `ASSEMBLED`.

## Operating modes

Declare your mode in the first line of every response before you touch a file.

- **Mode A -- Module Map.** Decompose a system into bricks and fix their contracts. Produces no implementation code at all.
- **Mode B -- Brick Loop.** Build exactly one brick. The default mode.
- **Mode C -- Assembly Ladder.** Join an `ACCEPTED` brick to the assembly and test the seam.
- **Mode D -- Carve-out.** Extract a brick from existing code without changing its behavior.

Pick by state: no map yet, Mode A. Map exists with a `PLANNED` or `CONTRACTED` brick next in order, Mode B. A brick just reached `ACCEPTED`, Mode C. Working inside code you did not write under this method, Mode D. If two modes seem to apply, take the earlier one.

## Workflow

### 1. Establish ground rules and declare the mode

Identify the language, test runner, existing layout, and how a single test file is executed here. Read the repository's own instructions and match its conventions -- this method governs granularity and contracts, not house style.

Confirm the module map's location (`dev/MODULE_MAP.md` by default, or wherever this repository keeps development documents) and read it if it exists. State the mode, the brick you are about to work on, and its current status. If the human's request implies building several bricks, say which one you will build and that you will stop after it.

### 2. Mode A -- draw the module map

Write no implementation code in this mode. None. The output is a map and a set of contracts.

Decompose by responsibility and rate of change, not by layer. Ask what each brick hides from its callers -- a good brick conceals a decision that might change; a bad one exposes a step in a procedure. Push every I/O concern to `SHELL` bricks at the edges and keep the decision-making in `CORE` bricks that never touch the outside world.

For every brick record: id, name, `CORE`/`SHELL`, one-sentence purpose, exact inputs with types and preconditions, exact outputs with types and postconditions, errors raised, dependencies, and status. Contracts are the deliverable here. Vagueness now becomes rework later, so state types concretely and name the failure cases.

Order the bricks leaves-first by dependency so that nothing is ever built against something unbuilt. Present the map, the build order, and the open questions, then stop for approval. Do not begin brick one because the map looks obvious. Follow [references/module-map.md](references/module-map.md).

### 3. Contract before code

Write the header block into the module file, with the signature and types, and nothing else implemented. This is `CONTRACTED`.

If the map's contract turns out to be wrong or underspecified, stop here and say so. Fixing a contract before implementation is cheap; discovering it after two dependent bricks exist is the failure this method exists to prevent.

### 4. Testbench before implementation

Write the sibling testbench next, before any implementation. It must fail. A testbench that passes against an unimplemented module is testing nothing.

Encode the contract as executable cases, not the implementation you are about to write: every documented output for a representative input, every boundary named in the preconditions, every error in `RAISES` asserted to actually raise, and at least one golden case whose expected output is written out in full. Add property tests for `CORE` bricks where an invariant is expressible. For `SHELL` bricks, test the contract against a fake and keep exactly one real smoke test that touches the actual resource.

Run it. Show the failure. This is `RED`. Details and the case taxonomy are in [references/testbench.md](references/testbench.md).

### 5. Implement the smallest brick that passes

Write the least code that satisfies the contract. No generality for imagined future callers, no configuration nobody asked for, no abstraction with one implementation.

Hoist the values a human will want to change into named constants at the top of the file and list them under `TUNING` with their range and effect. Comment every non-obvious branch with why it exists and every constant with where its value came from. Fill in `DECISIONS` as you make them, not afterward from memory.

If you find you need something outside the contract -- another input, a side effect, a dependency on an unbuilt brick -- stop. Report what the contract is missing and propose the smallest change. Do not widen the contract silently. That single habit is the difference between this method and a normal agent run.

### 6. Prove it

Run the testbench and show the exact command, exit code, and output. Every case passes, or the brick is not `GREEN`. Never weaken a test to make it pass; if a case was wrong, say that explicitly and justify the change against the contract.

Then run the demo entry point so a human can watch the brick work on real input and read the result. The demo is a sanity check for a person, never a substitute for the testbench, and never cited as test evidence.

Run the bundled checker before reporting:

```bash
python3 <skill-directory>/scripts/check_module.py <path-to-module>
```

It verifies the header is complete, the testbench exists, the size caps hold, a `CORE` brick has no I/O imports, and no stub markers remain. A `FAIL` is a defect in your brick, not a nuisance.

### 7. Hard stop and hand over

Report, then stop. The report contains:

- the brick, its kind, and its final contract;
- decisions made, each with its alternative and the trigger that would reverse it;
- the exact test command, its exit code, and its output;
- what the demo printed;
- **how to tweak this** -- which lines carry the choices most likely to need changing, which constants are safe to adjust, and which test catches a break in each;
- what remains assumed, unhandled, or outside the contract.

Then stop. Do not start the next brick, do not tidy a neighboring file, do not pre-build anything. Wait for the human to mark the brick `ACCEPTED`, request a tweak, or issue a contract change. A brick you accepted yourself is not accepted.

### 8. Mode C -- the assembly ladder

When a brick is `ACCEPTED`, join it to the assembly and prove the seam before anything else is built.

Write a seam test that runs real data across the boundary between the new brick and each brick it connects to -- the new brick's actual output fed to its consumer's actual input, no fakes. This catches the contract mismatch that unit tests structurally cannot see: both sides pass their own tests and disagree about what the data means.

Keep the assembly tests cumulative. Rung N runs every rung before it. Two bricks, then three, then four, and the whole ladder re-runs each time. When a rung breaks, the brick that just joined is the suspect and the ladder tells you exactly where.

Add a golden artifact for the assembly's end-to-end output where one is meaningful. Report the full ladder result, then stop.

### 9. Mode D -- carve a brick out of existing code

Do not refactor first. Characterize first.

1. Pin current behavior with golden-master tests over the region you intend to touch, capturing what it actually does including behavior that looks wrong. You are recording reality, not endorsing it.
2. Find the seam -- the narrowest place where behavior can be substituted without editing logic.
3. Write the contract for the brick you want to exist, as in Mode A.
4. Extract behind that contract and repoint the old call site at the new brick. The golden master must pass **unchanged**. If it does not, you changed behavior during extraction; revert and re-cut.
5. Only now write the real testbench and improve what is inside the brick, with the golden master still standing.
6. Repeat one brick at a time, strangler-fig style, so the old structure shrinks as the new one grows.

Fixing a bug you find during extraction is a separate brick with its own sign-off. Bundling a fix into an extraction destroys the one property that makes carve-outs safe. Follow [references/carve-out.md](references/carve-out.md).

### 10. Contract changes, rework, and the batch escape hatch

A contract change is issued by the human, never taken by you. It resets the affected brick and every downstream brick to `CONTRACTED`, and their seam tests come off the ladder until they are rebuilt. Say plainly which bricks a proposed change invalidates before the human decides.

On rework, change something real: the contract, the decomposition, the test cases, or the approach. Re-running the same implementation against the same failing test is not a retry. After two failed attempts on one brick, stop and report that the brick is probably mis-cut, with a proposed re-split.

The human may pre-authorize a run with `BATCH <ids>` for small bricks whose contracts are already approved. In batch you still write contract then testbench then implementation for each brick in order, and you still halt immediately on any failing test, any needed contract change, any brick that exceeds a hard limit, and any surprise. Batch shortens the reporting cadence; it never relaxes the method.

### 11. Close out the run

Update the module map with final statuses. State the assembly ladder's current height and result, which bricks are `ACCEPTED`, which are merely `GREEN` and awaiting sign-off, what is still `PLANNED`, and the next brick in build order.

Report honestly. Untested platforms, skipped cases, unproven assumptions, and known limits stay visible. Never call a skipped, blocked, or unavailable check a pass.

## Pitfalls

- **Scaffold sprawl:** empty directories, config, and placeholder files appear before any brick needs them.
- **Whole-system drift:** a single-brick request quietly becomes four bricks and a framework.
- **Contract drift:** the implementation grows an input or a side effect the header never mentions.
- **Testbench theater:** cases assert what the code does rather than what the contract promises, so the tests can never fail.
- **Green by narrowing:** a failing case is weakened or deleted instead of the implementation being fixed.
- **Mock theater:** every dependency is faked, nothing real is ever exercised, and the seam breaks on first contact.
- **Demo laundering:** the `__main__` demo printing plausible output is cited as test evidence.
- **Leaky black box:** a caller reaches past the entry point into internals, and the brick can no longer be changed.
- **Brick creep:** the module drifts past the size caps and quietly becomes a subsystem with no seam tests.
- **Comment noise:** every line is narrated, the real reasons are nowhere, and reviewers stop reading.
- **Decision amnesia:** `DECISIONS` is filled in afterward with restated code and no genuine alternative.
- **Stub debt:** unbuilt bricks get placeholders so the current one runs, and the placeholders survive to production.
- **Ladder skipping:** bricks are accepted individually and joined without seam tests, hiding contract mismatches until integration.
- **Big-bang carve-out:** legacy code is restructured before its behavior was characterized, and no one can tell what broke.
- **Silent acceptance:** the agent declares its own brick accepted and moves on.

## Verification checklist

- [ ] The mode was declared and matched the actual work performed.
- [ ] Exactly one brick was built, or an explicit `BATCH` authorization covered the run.
- [ ] The contract was written and shown before any implementation existed.
- [ ] The testbench was written before the implementation and observed failing.
- [ ] The header is complete: purpose, kind, contract, guarantees, tuning, decisions, limits, testbench.
- [ ] `DECISIONS` names a real alternative and a revisit trigger for every non-trivial choice.
- [ ] The brick is within the public-symbol, input, line, and dependency limits.
- [ ] `CORE` bricks are pure and `SHELL` bricks hold no business logic.
- [ ] Contract cases, boundaries, error paths, and at least one golden case all pass, with the command and exit code shown.
- [ ] The demo entry point ran and produced real, readable output.
- [ ] `check_module.py` passed on the brick.
- [ ] The seam test ran and the full cumulative ladder passed after joining.
- [ ] The report included how to tweak the brick and what remains assumed.
- [ ] The agent stopped and left acceptance to the human.

## Reference loading map

- Brick anatomy, header spec, `CORE`/`SHELL` rules, size limits, and comment discipline: [references/module-contract.md](references/module-contract.md). Read before writing any brick.
- Testbench design, case taxonomy, golden and property testing, seam tests, and the assembly ladder: [references/testbench.md](references/testbench.md). Read before writing any test.
- Decomposition heuristics, map format, build ordering, and decomposition anti-patterns: [references/module-map.md](references/module-map.md). Read in Mode A.
- Characterization, seams, extraction, and strangler sequencing: [references/carve-out.md](references/carve-out.md). Read in Mode D.
- Language recipes -- layout, contract expression, runner commands, demo idiom, golden and property libraries: [references/language-python.md](references/language-python.md), [references/language-typescript.md](references/language-typescript.md), [references/language-go.md](references/language-go.md), [references/language-rust.md](references/language-rust.md). Read the one that matches the project.
- The established practice each rule comes from, for judgment calls the rules do not cover: [references/method-lineage.md](references/method-lineage.md).
