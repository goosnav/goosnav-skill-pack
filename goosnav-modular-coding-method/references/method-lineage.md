# Where these rules come from

Read this when a judgment call is not covered by the rules. Each source below prescribes something specific; knowing what it actually says is usually enough to resolve the case.

## Decomposition

**D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972).** The founding argument for information hiding. Parnas compared two decompositions of the same program: one split by processing step, one split by hidden design decision. The step-based split looked reasonable and was far worse to change, because every modification crossed every module. The criterion he proposed is the one this method uses: **each module hides a decision that might change**, and its interface reveals as little as possible about how it works.

Applies to: whether a proposed brick is real. Ask what it hides. "A step" is the wrong answer.

**D. L. Parnas and P. C. Clements, "A Rational Design Process: How and Why to Fake It" (1986).** Design never actually proceeds rationally, but the documentation should be written *as if* it had, because the reader needs the rationale, not the history. This is why `DECISIONS` records the chosen option and the alternative rather than the sequence of confusions that produced it.

## Contracts

**Bertrand Meyer, Design by Contract (Eiffel, 1986).** A routine's obligations are symmetric: the caller guarantees the preconditions, the routine guarantees the postconditions, and the class invariant holds across both. The value is not runtime checking -- it is that responsibility is assigned unambiguously, so a failure has exactly one owner. When a `CORE` brick's precondition is violated, the caller is wrong; that is why bricks assert rather than defensively coerce.

Applies to: whether to validate an input or assert it. Validate at `SHELL` boundaries where data is untrusted; assert inside `CORE` where the contract says the caller is responsible.

## Purity and structure

**Gary Bernhardt, "Boundaries" (2012) -- functional core, imperative shell.** Push decisions into pure functions and I/O to a thin outer layer. The pure core is testable without mocks, exhaustively and fast; the shell is so thin that a small number of integration tests cover it. This is the whole justification for `CORE`/`SHELL`, and for why the method insists that a brick declare which it is.

Applies to: where a piece of logic goes. If you are mocking a lot to test something, logic has leaked into a shell brick.

**The Unix philosophy (McIlroy, Pike, Kernighan).** Do one thing well; expect the output of one program to become the input of another; write programs that are individually runnable. The demo entry point and the single-responsibility rule both come from here.

## Testing

**Hardware testbenches (VHDL/Verilog).** A testbench is a separate module that instantiates the device under test, drives stimulus, and checks outputs, with no visibility inside the DUT. The separation is structural, not a matter of discipline -- which is exactly the property this method wants and why the test file is a sibling rather than an inhabitant.

**Kent Beck, Test-Driven Development (2002).** Write the failing test first. The point is not coverage; it is that writing the test forces you to be the caller before you are the implementer, and awkwardness discovered then is design feedback arriving while it is still free.

**Michael Feathers, Working Effectively with Legacy Code (2004).** Legacy code is code without tests. A *seam* is a place where behavior can be changed without editing at that place. *Characterization tests* record what code actually does, not what it should. All three ideas are the whole of Mode D.

**Llewellyn Falco, approval / golden-master testing.** Pin the entire output rather than asserting properties of it, so whole-shape regressions surface in a reviewable diff. The corresponding hazard is regenerating the golden to make a failure disappear, which is why this method treats every golden change as requiring a stated reason.

**QuickCheck (Claessen and Hughes, 2000), and its descendants Hypothesis, fast-check, proptest.** Assert invariants over generated inputs rather than examples you chose. Valuable precisely because it explores the inputs you did not think of -- which is where the last twenty percent tends to live.

**Consumer-driven contract testing (Pact); Martin Fowler, "Integration Contract Tests".** Two components can each pass their own tests while disagreeing about the meaning of what crosses between them. Only a test that runs real data across the real boundary catches it. This is the seam test, and the reason the assembly ladder exists at all.

## Change and rationale

**Michael Nygard, "Documenting Architecture Decisions" (2011).** An ADR records context, the decision, alternatives considered, and consequences -- one per decision, immutable once made, superseded rather than edited. This method embeds a compressed ADR in the module header, on the theory that a rationale living next to the code gets read and one living in a separate directory does not.

**Martin Fowler, "Strangler Fig Application" (2004).** Grow the replacement around the existing system and let the old one shrink, rather than rewriting in parallel and cutting over. Mode D's sequencing is this pattern at module scale.

## The failure modes

**Tom Cargill's ninety-ninety rule.** "The first 90% of the code accounts for the first 90% of the development time. The remaining 10% accounts for the other 90%." The user-facing version of this method's premise: an agent's output is mostly right and the remainder is most of the work, so optimize the process for making that remainder findable.

**Foote and Yoder, "Big Ball of Mud" (1997).** Systems without discernible architecture arise incrementally, from expedient local decisions, each individually defensible. Nobody chooses a ball of mud; it accretes. The one-brick-per-turn stop exists because the accretion is invisible from the inside while it is happening.

## Resolving a conflict between sources

When two of these pull in different directions, prefer, in order: the contract the caller depends on; the ability of a human to understand and change the brick; the established convention of the project's language; and only then the general rule. This method exists to keep code legible to the person who has to finish it. A rule that makes a specific brick harder to understand is being applied wrongly.
