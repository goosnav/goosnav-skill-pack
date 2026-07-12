# Decision rules and escape hatches

The default stack exists to reduce agent drift. Deviate only when one of these conditions is real and documented.

## Valid reasons to deviate

- required platform or hardware is unsupported;
- a library license conflicts with the product model;
- measured performance cannot meet requirements;
- security/compliance requirements demand another component;
- a required SDK exists only in another language/runtime;
- existing code and migration cost strongly favor retention;
- operational cost or provider limits are demonstrated, not imagined;
- the user's explicit requirement selects another technology.

## Invalid reasons to deviate

- “more modern,” “more scalable,” or “cleaner” without evidence;
- agent familiarity or preference;
- a speculative future feature;
- avoiding the work of understanding the existing code;
- replacing a stable dependency during an unrelated feature;
- premature microservices;
- chasing one-codebase purity across web, desktop, and mobile.

## Decision test

For a proposed deviation write:

1. active constraint;
2. default option;
3. proposed option;
4. evidence;
5. effect on M1/M2/M3/M4;
6. build/packaging implications;
7. security and licensing implications;
8. rollback/migration path.

Choose the lowest-complexity option that satisfies the current and near-certain requirements.

## Existing repositories

Do not rewrite a working application into the default stack automatically.

1. map existing boundaries;
2. identify actual blockers to the active milestone;
3. add governance, tests, and stable seams first;
4. migrate incrementally only where benefits exceed risk;
5. preserve user data and compatibility;
6. use strangler/adaptor patterns instead of a big-bang rewrite.

## “Separate folders” rule

Use a monorepo by default because shared contracts, tests, and coordinated releases matter. Split into separate repositories only when there is a real ownership, security, deployment, licensing, or lifecycle boundary.

Within the monorepo, keep platform surfaces in separate top-level folders and prevent reverse dependencies into UI/platform code.
