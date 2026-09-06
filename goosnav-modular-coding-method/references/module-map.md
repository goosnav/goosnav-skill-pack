# The module map

Read this in Mode A. The output of Mode A is a map and a set of contracts, and no implementation code whatsoever.

## Why the map comes first, and why it is not scaffolding

There is a real tension in this method. Building brick by brick from the bottom risks building bricks that do not compose. Building the whole skeleton first is exactly the failure mode this method rejects. The resolution: **fix the interfaces up front, build the implementations one at a time.** The map is contracts and dependency order -- it is not directories, not stub files, not config, not a framework. Nothing is created on disk except the map document itself.

That distinction is the whole game. Deciding what the bricks are is cheap and reversible. Creating forty files that half-exist is neither.

## Decomposing

Decompose by **responsibility and rate of change**, not by layer. Layers ("models, views, controllers") produce bricks that must all change together for any real feature, which defeats the purpose.

The Parnas question is the sharpest tool available: *what does this module hide?* A good brick conceals a decision that might change -- a file format, a pricing rule, a vendor API, a storage choice. A bad brick exposes a step in a procedure -- "step two of checkout" -- and forces every caller to know the sequence.

Practical heuristics:

- **Draw the I/O boundary first.** Everything that touches the outside world becomes `SHELL` bricks at the edges. Everything that decides anything becomes `CORE` bricks in the middle. Most systems have far fewer shell bricks than people expect.
- **Follow the data.** Trace one real input from arrival to result. Each transformation with a nameable output is a candidate brick.
- **Split where the types change.** A place where data changes shape is usually a seam worth making explicit.
- **Split where change rates differ.** Code that changes weekly should not share a file with code that has not changed in a year.
- **One reason to change per brick.** Two reasons means two bricks.

Right-size against the limits in `module-contract.md`. A brick that will obviously exceed two hundred lines is too big; a brick that is one three-line function called from one place is probably too small and should fold into its caller. When unsure, prefer slightly too small -- oversized bricks are the failure this method exists to prevent, and merging two bricks is easier than splitting one that grew.

## Contracts are the deliverable

Vagueness in the map becomes rework in the build. For every brick, record:

| Field | Content |
| --- | --- |
| `id` | Stable short id, e.g. `B03`. Referenced by build order, seam tests, and commits. |
| `name` | File-level name in repository convention. |
| `kind` | `CORE` or `SHELL`. |
| `purpose` | One sentence, one verb. |
| `in` | Each input: name, concrete type, precondition. |
| `out` | Concrete type and postcondition. |
| `raises` | Each error and the condition that triggers it. |
| `deps` | Brick ids this one calls. |
| `status` | `PLANNED` / `CONTRACTED` / `RED` / `GREEN` / `ACCEPTED` / `ASSEMBLED`. |

Write concrete types. "A record of the transaction" is not a contract; "`Transaction{id: str, cents: int, posted_at: date}`" is. If the type does not exist yet, define it in the map -- shared boundary types are map-level decisions, not brick-level ones.

## Map file format

Default location `dev/MODULE_MAP.md`, or wherever the repository already keeps development documents.

```markdown
# Module map: <system>

## Contract
For <user>, this system turns <input> into <output>, complete when <signal>.

## Bricks
### B01 parse_ledger -- CORE -- ACCEPTED
Purpose: Turn raw ledger text into validated transactions.
IN:  raw: str -- UTF-8, may be empty
OUT: list[Transaction] -- ordered as in source, may be empty
RAISES: LedgerFormatError when a non-blank line has fewer than 3 fields
DEPS: none
### B02 ...

## Build order
B01, B02, B04, B03, B05   (leaves first; B03 needs B02 and B04)

## Assembly ladder
rung 1: B01
rung 2: B01 -> B02
...

## Open questions
Q1: ...
```

## Build order

Order leaves-first by dependency -- topologically, so nothing is ever built against something unbuilt. That constraint is not bureaucratic: it is what makes every brick testable the moment it exists, with no mocks standing in for modules that do not exist yet.

If the dependency graph has a cycle, the decomposition is wrong. Break it by extracting the shared concept into its own brick that both sides depend on, or by inverting one direction with a passed-in function or interface. Do not proceed with a cycle in the map.

When two bricks are independent, build the riskiest one first. The brick most likely to invalidate the map should be discovered early, while the map is still cheap to change.

## Importing an existing specification

If the repository already has a `nasa-v-model` specification suite, or any architecture document with defined components, derive the map from it rather than re-deriving the system. Map each specified component to one or more bricks, carry the specified interfaces into the contracts verbatim, and record any place where the specification is too vague to implement as an open question rather than inventing the detail silently.

## Decomposition anti-patterns

- **Layer slicing:** bricks named for tiers, so every feature touches all of them.
- **God brick:** one module everything depends on, usually named `utils`, `helpers`, or `common`.
- **Anemic bricks:** a dozen one-line modules that only pass data through, adding indirection and no hiding.
- **Premature interface:** an abstraction with exactly one implementation, invented for an imagined second one.
- **Sequence exposure:** bricks named `step_one`, `step_two`, forcing callers to know the order.
- **Shared mutable state:** two bricks communicating through a global instead of through their contracts. There is no contract that describes this, which is the tell.
- **Map as scaffolding:** creating the files. The map is a document. Nothing else exists yet.

## Stop and get approval

Present the map, the build order, the ladder plan, and the open questions. Then stop. Do not start brick one because the map looks obvious -- the map is the cheapest thing in the project to change, and the last moment it is free.
