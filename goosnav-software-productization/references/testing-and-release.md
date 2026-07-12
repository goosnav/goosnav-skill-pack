# Testing, verification, packaging, and release evidence

## Test pyramid by boundary

### Domain unit tests

Fast, deterministic, no network, no filesystem except isolated temp paths. Cover invariants, calculations, policy, and failure behavior.

### Contract tests

Verify:

- application-service inputs/outputs;
- OpenAPI schema and generated client compatibility;
- persistence repository behavior;
- AI-provider adapter normalized behavior;
- CLI JSON schemas and exit codes;
- billing/entitlement state transitions.

### Integration tests

Exercise real SQLite, test Postgres, filesystem workspaces, local API, queue adapters, and external-provider sandboxes/mocks.

### End-to-end tests

Use the actual browser/desktop/mobile surface for primary workflows. Do not replace all end-to-end evidence with mocked component tests.

### Packaging tests

For each supported target:

- build from a clean CI runner;
- install/extract;
- launch;
- sidecar health and shutdown;
- create/save/reopen project;
- log/config/data paths;
- update/migration behavior;
- uninstall/remove;
- artifact checksum.

## Canonical checks

A project should expose canonical commands through scripts or task runner, for example:

```text
setup
format
lint
check-types
test
test-integration
test-e2e
build
package
run
smoke
```

Document exact commands in `AGENTS.md` and `SETUP.txt`. Agents must run the relevant commands after changes and report real results, not “should pass.”

## Clean-environment requirement

At every release candidate, test from outside the developer's warm environment:

- fresh clone;
- no untracked dependency cache assumed;
- `.env` absent unless explicitly created from example;
- clean database and workspace;
- release artifact on a machine/user account that did not build it.

## Cross-platform CI

Use a matrix for supported operating systems and architectures. At minimum:

- Windows current supported release;
- macOS Apple Silicon; add Intel only if product evidence requires it;
- Ubuntu LTS or the chosen Linux baseline.

CI build success is necessary but not sufficient. GUI launch and OS security prompts require targeted manual smoke testing.

## Release evidence file

For each candidate record:

- version and commit;
- milestone/slice;
- artifact names, sizes, hashes;
- build environment;
- tests and results;
- migrations;
- supported/untested targets;
- signing/notarization status;
- known issues;
- rollback/recovery;
- user acceptance result.

## Performance

Establish a small representative benchmark for the primary workflow before optimization. Profile first. Use C++/Rust acceleration only when the benchmark demonstrates a material bottleneck and the native boundary can be tested and packaged reliably.

## Failure testing

Test at least:

- missing/invalid API key;
- provider timeout/rate limit/malformed response;
- disk full or permission denied;
- corrupt project/archive;
- interrupted write/migration;
- port collision/sidecar crash;
- unavailable network;
- duplicate CLI invocation/idempotency;
- webhook replay/out-of-order event;
- quota exhausted/global kill switch;
- mobile background/interruption.

## User acceptance checklist

Keep it short and task-oriented:

1. exact artifact/command to launch;
2. exact primary workflow to perform;
3. expected result;
4. one persistence/restart check;
5. one failure/recovery check;
6. where to find logs/support data;
7. approval phrase or issue-report format.
