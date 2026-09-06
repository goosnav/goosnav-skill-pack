# Testbench design

Read this before writing any test. It defines what a brick's tests must cover and what counts as evidence.

## The DUT model

The term comes from hardware. A testbench in VHDL or Verilog is a separate module that instantiates the device under test, drives it with stimulus, and asserts on its outputs. The DUT has no idea it is being tested; the testbench reaches nothing inside it. That discipline is exactly what a software black box needs, and it is why this method keeps the testbench in its own file rather than inside the module.

Consequences worth taking literally:

- The testbench imports the brick through its public entry point only. If a test needs a private helper, either the helper is really public, or the test is wrong.
- The testbench asserts the **contract**, not the implementation. Rewriting the internals without touching the tests should leave every test passing. If a refactor breaks tests that the contract did not change, the tests were measuring the wrong thing.
- The testbench is the gate. The demo is not.

## Two artifacts, two jobs

**The sibling test file** is the gate. It runs under the project's real test runner, it runs in CI, it fails the build. This is where correctness is decided.

**The demo entry point** is for the human. It runs the brick on a real input and prints the result so a person can look at it and say "yes, that is what I wanted" -- the judgment a test cannot make. It is a sanity check and a living usage example. It is never cited as test evidence, never counted as coverage, and never the reason a brick is called `GREEN`.

Keep the demo small: one representative input, the call, and readable output. If it grows fixtures and branches, it is turning into a test suite in the wrong file.

## Case taxonomy

Every brick's testbench covers these categories. Missing categories are reported, not silently skipped.

**Contract cases.** One per documented behavior in `CONTRACT`. Representative input, exact expected output. These are the promises.

**Boundary cases.** Every precondition names a boundary; test both sides of it. Empty input, single element, maximum size, zero, negative, the first and last valid value, off-by-one on any range. Most brick defects live here.

**Error cases.** Every entry in `RAISES` gets a test asserting that the specific error is raised on the specific condition. Assert the error type and, where the contract promises it, the message content. An error path with no test is an error path that does not work.

**Golden cases.** At least one case whose full expected output is written out and compared verbatim -- a fixture file, a snapshot, or an inline literal for small outputs. Goldens catch the whole-shape regressions that assertion-by-assertion tests miss, and they make output changes visible in the diff instead of invisible in a passing suite. Review every golden change on purpose; regenerating a golden to make a test pass is the same sin as weakening an assertion.

**Property cases** for `CORE` bricks where an invariant is expressible. Round-trips (`decode(encode(x)) == x`), idempotence, ordering invariance, conservation, monotonicity, and "never raises on any valid input" are the common ones. Property tests explore the input space you did not think of, which is precisely the space where the last twenty percent hides.

**Fake-and-smoke** for `SHELL` bricks. Test the contract against a fake resource for speed and determinism, then keep exactly one test that touches the real thing. A shell brick tested only against fakes has been proven to work against your beliefs about the resource, not the resource.

## Writing the testbench first

It fails before the implementation exists. Show that failure. A testbench that passes against an unimplemented module is testing nothing, and this is the single easiest way to catch it.

Red-green is not ceremony here. Writing the tests first forces you to use the contract as a caller before you commit to an implementation, and the awkwardness you feel while doing that is design feedback arriving at the only moment it is still cheap.

Rules while going green:

- Never weaken a case to make it pass. If a case was genuinely wrong, say so explicitly and justify the change against the contract, in the report.
- Never delete a failing case. Fix the brick or fix the contract.
- Never add a test that asserts current behavior you have not reasoned about. That is a golden master, and it belongs in Mode D, not here.

## Seam tests and the assembly ladder

Unit tests structurally cannot catch a contract mismatch: both bricks pass their own tests while disagreeing about what the data means. Producer emits cents, consumer assumes dollars, both are green, the system is wrong. This is the failure that consumer-driven contract testing exists to prevent, and it is why the ladder matters.

**A seam test** runs real data across a real boundary. The producer brick's actual output is fed to the consumer brick's actual input, with no fakes between them. Assert on what comes out the far side. One seam test per connection in the module map.

**The ladder is cumulative.** Rung N runs every rung before it:

```text
rung 1   brick A alone
rung 2   A -> B, plus rung 1
rung 3   A -> B -> C, plus rungs 1-2
rung 4   the above plus D's seam, plus rungs 1-3
```

Every time a brick joins, the whole ladder runs. When a rung breaks, the brick that just joined is the prime suspect and the ladder localizes the fault immediately -- which is the property that makes brick-by-brick building faster than big-bang integration, not slower.

Add an end-to-end golden artifact for the assembly's output once there is a meaningful output to pin. Keep it in version control so its diffs are reviewable.

## What counts as evidence

Cite the exact command, the working directory if it is not obvious, the exit code, and the relevant output. Not "tests pass." Not a summary of what you believe happened.

- A skipped test is not a pass. Report it as skipped and say why.
- A test that could not run because the runner was missing is `UNVERIFIED`, not green.
- A demo that printed plausible output proves nothing about correctness.
- Coverage percentage is not evidence of contract coverage. A brick can be at one hundred percent line coverage with every error path untested for the error it actually raises.

State untested platforms, unavailable dependencies, and unexercised paths explicitly in the report. The value of this method comes from knowing exactly which bricks are solid, and that value is destroyed by one overstated claim.
