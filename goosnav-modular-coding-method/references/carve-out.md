# Carve-out: extracting bricks from existing code

Read this in Mode D, whenever you are working inside code that was not built under this method.

## The rule that makes it safe

**Characterize before you change.** Not refactor-then-test. Not "clean it up while I'm in here." The one property that makes a carve-out safe is that you can prove behavior did not change, and you can only prove that if you captured the behavior first.

This is Feathers' definition of legacy code: code without tests. The problem is not age or ugliness, it is the absence of a safety net. Build the net first, every time.

## The five steps

### 1. Characterize

Write golden-master tests over the region you intend to touch. Feed it real inputs, capture whatever it actually produces, and pin that as expected.

You are **recording reality, not endorsing it**. If the code rounds wrong, mis-handles empty input, or emits a typo in an error string, the golden master records the wrong rounding, the mishandling, and the typo. Note them as observed defects to fix later, as their own bricks, with their own sign-off. Do not fix them now. A carve-out that also fixes bugs cannot be verified, because a failing golden master no longer tells you whether you broke something.

Get enough inputs to cover the paths you are about to move. If the region has branches you cannot reach with any input you can construct, say so -- that unreachable region is a risk you are carrying into the extraction, and it belongs in the report.

Where output is not a clean value -- it writes files, calls a service, mutates a database -- capture the effects instead: the written bytes, the request payloads, the resulting rows. Characterize what is observable.

### 2. Find the seam

A seam is a place where you can change behavior without editing the logic at that place. Look for a function boundary, a class boundary, an injected argument, a module import, an interface. The narrowest seam that isolates the behavior you want is the right one.

If there is no seam, make one -- and make *only* that. Extracting a block of code into a local function, changing nothing else, is a safe move you can verify immediately against the golden master. Do that as its own step before attempting the real extraction.

### 3. Write the contract

Write the header block for the brick you want to exist, exactly as in Mode A: purpose, kind, contract with concrete types, guarantees, decisions, limits.

Write it for the brick you *want*, not a transcription of the mess you have. The contract is a target. Where the existing behavior violates the contract you want, that gap is the work -- record it in `LIMITS` and address it after extraction, as a separate brick.

Declare `CORE` or `SHELL` here. Most valuable carve-outs pull pure decision-making out of a function that is doing I/O and logic at once: the logic becomes a `CORE` brick, the remaining I/O stays behind as a `SHELL` brick.

### 4. Extract and repoint

Move the behavior into the new brick. Repoint the old call site at it. Change nothing else -- no renames of unrelated things, no formatting sweeps, no dependency upgrades, no "while I'm here."

**The golden master must pass unchanged.** Not updated, not regenerated, not "adjusted for the new structure." Unchanged. If it fails, you changed behavior during extraction. Revert and re-cut with a narrower seam. Do not debug forward from a failing golden master; the whole point of the net is that you get to step back onto solid ground.

### 5. Test properly, then improve

Now write the real testbench for the new brick, per `testbench.md`: contract cases, boundaries, error paths, goldens, properties. This is the first point where you are testing what the brick *should* do rather than what the old code *did*.

Now, and only now, improve the inside of the brick. The golden master still stands as an outer guard and the new testbench guards the contract. Fix the defects you noted in step 1 here, one at a time, each one visible as a deliberate golden-master change with a stated reason.

## Sequencing across a whole codebase

Strangler fig: the new structure grows inside the old one, and the old one shrinks, until it is gone. Never a parallel rewrite, never a big-bang cutover.

One brick per turn applies with full force here. Report after each extraction and stop. The temptation to keep going is strongest in legacy work, because the next mess is always visible from where you are standing, and giving in is how a bounded extraction becomes an unreviewable diff.

Order the work by risk and value:

1. Behavior that is about to change anyway -- extraction pays for itself immediately.
2. Behavior that is central and frequently misunderstood.
3. Pure logic tangled up with I/O -- the highest ratio of test value to extraction effort.
4. Everything else, opportunistically, when you are already in the file for another reason.

Leave stable, working, rarely-touched code alone. Not everything needs to be a brick. Extraction has a cost and untouched working code has no defect you are being paid to find.

## Reporting a carve-out

Beyond the standard brick report, state:

- what the golden master covers and, honestly, what it does not;
- paths you could not reach with any constructed input;
- observed defects recorded but deliberately not fixed, each as a proposed follow-up brick;
- what still calls the old path, if the extraction was partial;
- whether the golden master passed unchanged, in those words.
