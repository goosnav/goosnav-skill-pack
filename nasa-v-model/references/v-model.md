# The NASA Systems Engineering "V" Model

The V model is a systems-engineering lifecycle that arranges the work as a "V" read left to right over
time. It is the backbone of NASA's systems-engineering practice (and of safety-critical engineering
generally) because it makes two things structural rather than optional: **decomposition before
implementation**, and **verification paired to every level of definition**.

Read the V like this:

- The **descending left arm** is *Definition and Decomposition*. You move from broad intent down to
  exact detail, one justified step at a time.
- The **bottom of the V** is *Implementation* -- the actual building (coding and unit test for
  software, fabrication for hardware).
- The **ascending right arm** is *Integration and Test*. You assemble and test upward, and each test
  activity is checked against the definition document at the **same height** on the left arm.
- A horizontal line at each height links a left-arm document to its right-arm test activity. **The
  plan for each right-arm activity is written while you are descending the left arm** -- not improvised
  later. That early pairing is the single most important property of the V.
Sitting above the whole V is the **Systems Engineering Management Plan (SEMP)**: how the project itself
is governed. Threaded through the entire V is **traceability**: the bidirectional links that prove
nothing is arbitrary.

## The left arm -- Definition and Decomposition

### 1. Concept of Operations (ConOps) -- the top

The ConOps captures **intent and need from the user's point of view**, with no solution detail. Who
are the users? What problem are they living with? How will they actually use the system, scenario by
scenario? What is the operating environment and what does success look like *in their terms*?

The ConOps is the **validation baseline**: at the very top of the right arm, *System Validation* asks
"did we build the right thing?" and answers it by checking the finished system against this document.
If the ConOps is vague, validation is meaningless, so it must describe success concretely.

### 2. System-Level Requirements -- what the system must do

Requirements translate ConOps intent into **testable "shall" statements** about the system as a whole:
functional behavior plus non-functional qualities (performance, security, privacy, accessibility,
reliability, compliance). Each requirement is atomic, unambiguous, and verifiable, and each carries a
parent need from the ConOps. These are the baseline for *System Verification* ("did we build it
right?") on the way up.

### 3. Subsystem Requirements / High-Level Design

Here the system is **decomposed into subsystems** and the broad solution shape is chosen: the
architecture, the technology stack (justified against requirements), the interfaces between
subsystems, and the data model. Each subsystem declares which system requirements it satisfies. The
baseline for *Subsystem Verification* on the way up.

### 4. Component Detailed Design -- the bottom of the left arm

The exact, build-ready specification of each component: responsibilities, interface/contract, data
structures, algorithms, error handling, and (when wanted) effort/size estimates. This is the level an
engineer -- or Claude Code -- builds directly from, with no further design decisions left implicit. The
baseline for *Component Verification* on the way up.

## The bottom -- Implementation

Coding and unit testing (or, for hardware, fabrication). Unit tests live here, closest to the code.
Everything above this point existed to make this step unambiguous; everything below... there is
nothing below -- this is where the V turns and starts coming back up.

## The right arm -- Integration and Test (verification and validation)

Each right-arm activity verifies against the left-arm document at the same height. Two distinct ideas
live here and are easy to confuse:

- **Verification** = "did we build the thing right?" -- conformance to the requirements/design at that
  level. (Component, Subsystem, and System Verification.)
- **Validation** = "did we build the right thing?" -- conformance to the user's actual need. (System
  Validation, at the top, against the ConOps.)
Ascending:

1. **Component Verification** -- each component meets its detailed-design spec (component verification
   *procedures*, written during step 4).
2. **Subsystem Verification** -- assembled subsystems meet the subsystem requirements (subsystem
   verification *plan*, written during step 3).
3. **System Verification** -- the integrated system meets the system-level requirements (system
   verification *plan*, written during step 2).
4. **System Validation** -- the finished system satisfies the ConOps and delivers the intended value
   in the operating environment (system validation *plan*, written during step 1).
Above System Validation sits the **Commissioned System -- Operations & Maintenance**: the deployed,
running system and its upkeep. In a software product this maps to launch, monitoring, support, and the
maintenance plan.

## Traceability -- the spine of the V

Traceability is the set of **bidirectional links** that connect the two arms:

- **Downward / forward:** each ConOps need produces one or more requirements; each requirement is
  satisfied by one or more design elements; each design element is realized in implementation.
- **Upward / backward:** each test traces to the requirement it verifies; each requirement traces to
  the need that justifies it.
A spec is "closed" when there are no orphans: no need without a requirement, no requirement without a
parent need *and* a verifying test, no design element without a requirement justifying it. The
traceability matrix (see `requirements-and-traceability.md`) is where this is recorded and audited.

## Why this beats an ad-hoc PRD or jumping straight to code

- Writing the verification plan *while* defining each level catches untestable or ambiguous
  requirements immediately -- when fixing them is cheap -- instead of at test time when it's expensive.
- Decomposing in small justified steps means every design decision has a traceable reason, so reviewers
  (and future maintainers) can understand *why*, not just *what*.
- Traceability gives change control teeth: when a requirement changes, the links show exactly which
  designs and tests are affected.