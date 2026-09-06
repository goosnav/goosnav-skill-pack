# Brick anatomy and the module contract

Read this before writing any brick. It defines what makes a module legal under this method.

## What a brick is

One brick is one module in one file that hides one decision. It is defined by its interface; callers may depend on the contract and on nothing else. Parnas's test still holds: ask what this module *hides*. If the answer is "a step in a procedure," the decomposition is wrong. If the answer is "a choice that might change," the brick is right.

A brick has four parts, all mandatory:

1. the contract header;
2. the implementation;
3. a sibling testbench that gates it;
4. a demo entry point that a human can run and watch.

## The header block

Written in the language's native comment or docstring syntax at the very top of the file, before imports where the language allows.

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

Field rules:

- **PURPOSE** is one sentence with one verb. If it needs "and," the brick does two things and must be split.
- **CONTRACT** states concrete types, not "data" or "object." Every precondition is a thing the caller must guarantee; every postcondition is a thing this brick guarantees in return. That symmetry is Design by Contract, and it is what makes the box black.
- **RAISES** is exhaustive for errors this brick originates. An error it merely propagates belongs in `LIMITS` instead.
- **GUARANTEES** is the negative space: what the brick will never do. `CORE` bricks always guarantee determinism and absence of I/O. Write the guarantee that a caller would otherwise have to read the source to discover.
- **TUNING** is the human tweak surface. Every value someone might reasonably want to change is a named constant here with its range and its effect, never a literal buried in a branch.
- **LIMITS** is where honesty lives. Unhandled encodings, unsupported sizes, assumed time zones, untested platforms. A brick with no limits is usually a brick whose limits were not looked for.

## DECISIONS: the part that matters

This is the ADR, embedded where the code is rather than in a document nobody opens. It is the single highest-value thing in the file for the human who has to change this in six months.

Every entry needs four parts:

```text
D2: chose a streaming parse over loading the whole file.
    Alternative: read fully into memory and parse once.
    Why not: inputs are user-supplied and unbounded; a 2 GB file would kill the process.
    Revisit if: inputs become bounded upstream, or profiling shows parse overhead dominates.
```

The revisit trigger is what separates a decision record from a rationalization. It tells a future reader the conditions under which this choice expires, so they can change it with confidence instead of guessing why it was made.

What does not belong here:

- Restated code. "Chose a loop to iterate the items" is not a decision.
- Padding. If there was no alternative worth considering, there was no decision. Leave it out.
- Style preferences the repository already settled.

Number entries `D1`, `D2` and keep them stable, so that review comments and commit messages can cite them.

## CORE and SHELL

Every brick declares exactly one kind. This is the functional-core / imperative-shell split made enforceable, and it is what lets functional discipline scale to a whole system.

**CORE bricks are pure.** Same input, same output, always. No file system, no network, no database, no clock, no randomness, no environment variables, no global mutable state, no logging to a real sink. Everything they need arrives as an argument. They are trivially testable, which is the entire point -- this is where the business logic goes, and business logic is what you actually need to test hard.

**SHELL bricks are adapters.** They own the messy outside: reading files, calling APIs, querying databases, reading the clock, generating randomness, writing output. They must contain **no business logic** -- no branching on domain meaning, no calculation, no policy. A shell brick fetches, hands the data to a core brick, and writes back what it gets. If you find yourself writing an `if` about what the data *means* inside a shell brick, that branch belongs in a core brick.

Injected nondeterminism is how a core brick gets what looks like an impure need: pass the timestamp in, pass the random seed in, pass the already-loaded config in. The caller -- a shell brick -- owns the impurity.

Violations to catch:

- A `CORE` brick that imports an I/O, network, time, or random module.
- A `CORE` brick that reads an environment variable or a module-level mutable.
- A `SHELL` brick with a computation or a domain decision in it.
- A brick that cannot say which kind it is. That brick is two bricks.

## Hard limits

| Limit | Soft | Hard |
| --- | --- | --- |
| Public symbols | 1 entry point | 3 |
| Inputs to the entry point | 3 | 5, then use a named struct |
| Implementation lines, excluding header and comments | 200 | 300, then stop and re-split |
| Dependencies on other bricks | 2 | 3, all `ACCEPTED` |
| Dependencies on unbuilt bricks | 0 | 0 |

At a hard limit, stop and report a proposed re-split. Do not negotiate with yourself about whether this brick is special. The limits exist because the failure they prevent -- a module too large to hold in your head -- is invisible from the inside while it happens.

A brick needing more than three collaborators is not a brick. It is an assembly, and it belongs in the module map as such.

## Comment discipline

The header carries *what* and the contract. Inline comments carry *why*, and only why.

Write a comment when:

- a branch exists for a non-obvious reason ("empty input reaches here from the CLI's `--all` flag, which yields no rows rather than erroring");
- a constant has a provenance ("30s: the upstream API's documented timeout plus one retry");
- an approach was chosen against the obvious one, and the reason is local rather than architectural (architectural ones go in `DECISIONS`);
- something looks like a bug but is not ("intentionally not sorted -- the caller's golden file depends on source order").

Do not write a comment that restates the code. `# increment the counter` above `count += 1` is noise, and noise is how a codebase teaches its readers to skip comments entirely. Well-commented does not mean densely commented; it means every comment carries information the code cannot.

Names do the rest of the work. A well-named function and a well-named variable remove the need for most comments, and the comment budget is better spent on the handful of places where intent genuinely cannot be read off the syntax.

## Naming

- Brick file name matches the entry point's responsibility, in the repository's existing convention.
- The entry point is a verb phrase: `parse_ledger`, `normalizeAddress`, `ComputeTax`.
- Types at the boundary are named nouns, not tuples or bare dicts. A named struct at the boundary is the difference between a contract and a suggestion.
- Testbench name follows the language's convention so the runner finds it without configuration.

## The stop condition

A brick is done when its testbench passes, its checker passes, its demo runs, and its header is complete and true. It is `GREEN`. It is not `ACCEPTED` -- only a human does that, and only after reading it.
