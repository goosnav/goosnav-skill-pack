---
name: goosnav-local-first-workbench
description: Build polished local browser workbenches with deterministic state, editable workflows, safe loopback routes, atomic persistence, portable artifact export, cross-platform launchers, and visual QA. Use for analyst consoles, creative tools, operations desks, review interfaces, and other local-first products that must feel dependable rather than like a developer demo.
version: 1.0.0
author: Goosnav LLC
license: Proprietary; internal use permitted
metadata:
  hermes:
    tags:
      - local-first
      - browser-workbench
      - deterministic-state
      - artifact-export
      - visual-qa
    related_skills:
      - goosnav-mvp-delivery
      - goosnav-software-productization
      - goosnav-parent-verification
---

# Overview

A workbench is a durable place to do a job: import material, inspect it, make edits, run a bounded operation, compare outcomes, save, reopen, and export. Build it as a local browser application with a deterministic application core and explicit filesystem boundaries. The browser is the interface, not the source of truth.

Default topology:

```text
native/repository launcher -> loopback server -> browser workbench
                                      |
                         application services
                         | state | artifacts | adapters
```

Keep canonical state on the server or in a versioned project artifact. Client state represents drafts, focus, selection, and temporary view preferences. Make every destructive or expensive action explicit. The user should be able to understand where data lives, recover from interruption, and carry useful work out of the tool.

## When to Use

Use for local research desks, simulation controls, content or dataset review tools, founder operations consoles, structured editors, batch processors with human review, and GUI wrappers around capable local services. It fits when privacy, offline use, direct file access, or zero-account startup matters.

Do not use it to disguise a command-line-only job with a decorative page. If no meaningful interaction exists, a CLI may be better. Use the software-productization skill when the main challenge is shipping the workbench as a universal customer artifact; use MVP Delivery when product scope and first vertical slice remain undefined.

## Workflow

1. **Define the work object and loop.** Name the smallest durable object: project, case, run, board, study, or workspace. Specify create/import, inspect, edit, execute, review, export, reopen, and failure recovery. State what is canonical and what may be discarded.

2. **Map trust and storage boundaries.** Choose an application-data root, user-approved import roots, project schema, export root, temporary space, and log location. Bind to `127.0.0.1` by default. Never treat “local” as “trusted”: malicious web pages, imported archives, filenames, and prompt content still cross boundaries.

3. **Make the core deterministic.** Inject clock, random seed, identifier source, and external providers where they affect results. Store operation inputs, normalized configuration, core version, seed, and output references. Replaying a deterministic operation with the same inputs must reproduce its substantive output.

4. **Design the project format.** Use a directory or archive with a versioned manifest, stable IDs, normalized relative paths, and explicit schemas. Write through a temporary sibling, flush when risk warrants, then atomically replace. Back up before migration. Reject traversal, symlinks escaping approved roots, oversized archives, and duplicate/case-conflicting paths.

5. **Build application services before routes.** Implement commands such as `create_project`, `import_items`, `update_item`, `run_workflow`, `undo_change`, and `export_artifact`. Put validation and invariants there. Routes translate HTTP input/output; they do not own business rules or filesystem policy.

6. **Define safe routes.** Separate reads from mutations. Validate bodies and content types, cap upload/request sizes, use timeouts/cancellation, and return stable error codes. Protect state changes with same-origin/CSRF controls plus a per-launch unguessable session. Never accept arbitrary shell commands or unrestricted absolute paths from the browser.

7. **Model edit state deliberately.** Give saved objects a revision or ETag. Submit the expected revision and reject stale edits with a recoverable conflict response. Autosave only small reversible changes; use explicit apply/run actions for expensive, destructive, or meaning-changing operations. Show dirty, saving, saved, failed, and conflict states.

8. **Build the workbench information architecture.** Prefer a clear frame: project switcher/header, primary canvas or table, contextual inspector, activity/status, and export/help. Keep the primary object visible while editing details. Preserve selection across non-destructive updates and offer keyboard operation where it materially accelerates repeated work.

9. **Handle every visible state.** Provide intentional first-run, empty, loading, progress, success, partial result, validation error, conflict, operational failure, offline/provider-unavailable, and recovery states. Do not use a spinner without an explanation and cancellation for long work. Keep errors near the failed action and include a safe next step.

10. **Make artifacts first-class.** Export a documented versioned artifact, not a screenshot of the UI. Include manifest, normalized inputs/configuration, substantive results, provenance, and checksums where integrity matters. Support reopen/import or supply a validator. Exclude secrets, absolute local paths, logs, caches, and unrelated source material by default.

11. **Add launch and lifecycle behavior.** Launchers resolve their own location, select a safe port atomically, open the browser, wait for readiness, reuse an existing healthy instance, surface logs/recovery, and supervise shutdown. Do not depend on the caller’s working directory. Claim only platforms actually exercised.

12. **Perform functional and visual QA.** Drive the real browser through create/import-edit-run-export-reopen. Inspect console and failed network calls. Capture representative states at narrow laptop and normal desktop widths. Check hierarchy, clipped controls, long names, focus, keyboard traversal, contrast, reduced motion, and zoom. Aesthetic quality is part of usability, but never substitutes for artifact correctness.

13. **Verify interruption and recovery.** Kill or cancel during import, save, and a long run. Confirm no canonical half-state, that temporary work is cleaned or recoverable, and that the next launch explains recovery. Test stale revision, corrupt project, read-only source, invalid export destination, and disk/permission failures proportionately.

14. **Document ownership.** State exact launch command, supported platforms, data and log paths, backup/export behavior, whether telemetry exists, how to quit, and how to reset safely. Keep secrets and user content outside the source repository.

## State and Artifact Contract

Use a manifest shaped to the product, with these minimum semantics:

```json
{
  "schema_version": 1,
  "project_id": "stable-id",
  "revision": 7,
  "created_at": "injected-time",
  "updated_at": "injected-time",
  "core_version": "1.2.0",
  "default_seed": 4182,
  "items": [],
  "runs": []
}
```

Timestamps may be metadata while deterministic result content uses a logical or injected clock. A run records the exact seed/config and references immutable input snapshots when later edits could change meaning. Exported relative paths use `/` separators and never escape the artifact root.

## Safe Route Minimum

- `GET /health/ready` reveals no secret and means mandatory initialization is complete.
- Reads are idempotent and bounded; pagination is explicit for large collections.
- Mutations require the launch session and validated origin.
- File selection is mediated by approved roots or a native chooser contract; browser text is not trusted as unrestricted path authority.
- Download headers sanitize filenames and set a precise content type.
- Error responses contain a stable code, safe message, and correlation ID, not raw tracebacks.
- A quit route is authenticated and graceful; it cannot be triggered cross-site.

## Pitfalls

- **Browser storage as database:** state disappears, diverges across tabs, or cannot migrate. Keep canonical project state server-side/artifact-based.
- **Nondeterminism leaks:** current time or random IDs make runs incomparable. Inject sources and record seeds.
- **Autosave everywhere:** expensive actions rerun or semantic edits become irreversible. Distinguish drafts, reversible edits, and commits.
- **Unsafe path convenience:** an API accepts any absolute path. Use approved roots, canonicalization, and traversal tests.
- **Pretty dead shell:** panels render but primary actions are placeholders. Verify through exported/reopened artifacts.
- **Export dumping:** archives contain secrets, local paths, caches, or source files. Assemble from a whitelist.
- **Desktop claims from local server tests:** loopback behavior alone does not prove launchers work across platforms.
- **Visual QA at one viewport:** long content and narrow screens break core controls. Test representative stress states.

## Verification Checklist

- [ ] Work object, canonical state, and edit/run loop are explicit.
- [ ] Clock, randomness, IDs, and provider behavior are controlled where determinism matters.
- [ ] Project writes and migrations are atomic, versioned, and recoverable.
- [ ] Imports and exports reject traversal and exclude secrets/absolute paths.
- [ ] State-changing routes use loopback, origin/CSRF, and per-launch protection.
- [ ] Dirty, saving, saved, conflict, empty, progress, error, and recovery states are visible.
- [ ] Primary browser flow succeeds and console/network failures were inspected.
- [ ] Export validates and reopens with substantive content and provenance.
- [ ] Interruption, corrupt input, permissions, and stale revisions have defined outcomes.
- [ ] Launchers resolve paths, open the browser, and shut down cleanly on tested platforms.
- [ ] Laptop/desktop visual QA, keyboard/focus, contrast, and long-content stress passed.
- [ ] Data, logs, reset, export, telemetry, and limitations are documented.

## Exact Recipe

Recipe: build a local experiment-review workbench.

1. Define a project as `project.json`, imported observations, immutable run snapshots, annotations, and exports. The core job is import observations, configure scoring, run, inspect outliers, annotate, and export a review bundle.
2. Implement `ScoreObservations` with injected clock and random source. Default fixture seed is `4182`; store algorithm/core version and normalized configuration beside each run.
3. Expose loopback routes for project reads, revision-checked edits, start/cancel run, and whitelist export. Require a launch-session header and same-origin mutation requests.
4. Build a table/canvas with persistent selection and an inspector for annotations. Show dirty/saved/conflict status; require explicit Run because scoring is meaningful. Add first-run fixture import visibly labeled fictional.
5. Export `review-bundle-v1.zip` containing a versioned manifest, normalized CSV, annotations, run config/results, and SHA-256 inventory. Write a validator that rejects extra files and reopens the project in a temporary directory.
6. Add launch scripts that choose a port, wait for readiness, open the browser, and use a temporary data root in verification.
7. Browser-smoke fixture import, edit, run, annotate, export, refresh, and reopen. Inspect console and network; then cancel during a run and force interruption during save to validate recovery.
8. Capture visual QA at 1280×800 and 1536×960 with long observation names, an empty project, a conflict, and an operational error. Record only tested platform launch claims.
