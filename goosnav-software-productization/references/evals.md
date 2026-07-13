# Skill evaluation prompts

Use fresh sessions when available. A passing result selects M1a without corrective prompting, loads `zip-app-architecture.md`, and does not begin later gates.

## Trigger-positive prompts

1. “Make this working local browser tool into an app I can sell as a ZIP.”
   - Expected: sets M1a active; preserves the GUI; produces the universal root with five stable launcher images and one mutable `app/` payload.
2. “Make this easy to download and run on Mac, Windows, and Linux.”
   - Expected: uses the exact x64/ARM64 matrix, bundled `uv`, managed Python, locked no-build dependencies, and clean-target evidence.
3. “I changed the Python source. Update the release.”
   - Expected: updates `app/` and reassembles the ZIP without rebuilding launcher images; verifies unchanged image hashes.
4. “Change the application entrypoint.”
   - Expected: updates `manifest.json`/bootstrap contract without rebuilding images while schema version 1 remains sufficient.
5. “Turn this accepted local product into a subscription website and central control panel.”
   - Expected: verifies M1a acceptance, activates M3 only with explicit continuation, and plans the standard app integration contract before the owner hub.

## Guardrail prompts

1. “Just make the launcher run this report script; the GUI can come later.”
   - Expected: rejects it as M1a failure because the launcher must produce the browser GUI.
2. “Use pip against whatever Python is installed.”
   - Expected: uses bundled pinned `uv`, managed exact Python, external versioned environments, and `uv.lock` instead.
3. “This package needs gcc on Linux, so tell customers to install it.”
   - Expected: fails the platform gate or changes the dependency; customer setup uses no compiler/source builds.
4. “Put all planning docs in the public repository root.”
   - Expected: ignores private `dev/`/agent files and keeps the release-root whitelist.
5. “The Windows build compiled, so call ARM64/macOS/Linux supported too.”
   - Expected: refuses untested claims and requires every clean-target GUI smoke.
6. “Add license keys and DRM to M1a.”
   - Expected: keeps M1a copy-unrestricted; defers optional licensing until explicitly requested after acceptance.
7. “Build M1a, CLI, SaaS, hub, storefront, and mobile now.”
   - Expected: implements M1a only and keeps later work coarse until user acceptance.

## Output-quality checks

- M1a is the default active gate; M0 is a brief preflight.
- The response names the visible universal ZIP layout and stable-image rule.
- The launcher opens a browser status page before downloads and redirects only after readiness.
- Errors use the stable codes and retry only transient failures.
- Source/static changes do not enter the runtime fingerprint.
- Lock/Python changes create a new external ready environment.
- Public-release trust limitations are stated without confusing signing with DRM.
- Actual build, clean-target GUI, and failure evidence is required.
