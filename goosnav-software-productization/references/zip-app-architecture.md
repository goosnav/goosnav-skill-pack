# M1a universal ZIP and stable launcher images

Read this reference completely before generating, changing, packaging, or testing an M1a launcher.

## Contents

1. Deliverable and invariants
2. Launcher protocol
3. Operating-system images
4. Dependency and runtime bootstrap
5. Process lifecycle and GUI contract
6. Failure contract
7. Packaging and repository rules
8. Acceptance matrix
9. Reusable build flow

## Deliverable and invariants

Ship one universal ZIP with this exact visible root shape:

```text
ProductName-M1a/
├── Open ProductName — macOS.app/
├── Open ProductName — Windows x64.exe
├── Open ProductName — Windows ARM64.exe
├── Open ProductName — Linux x86_64.AppImage
├── Open ProductName — Linux ARM64.AppImage
├── README.txt
├── LICENSE.txt
└── app/
    ├── pyproject.toml
    ├── uv.lock
    ├── .python-version
    ├── src/
    ├── static/
    └── launcher/
        ├── manifest.json
        ├── bootstrap.py
        ├── tools/
        │   ├── macos-x64/uv
        │   ├── macos-arm64/uv
        │   ├── windows-x64/uv.exe
        │   ├── windows-arm64/uv.exe
        │   ├── linux-x64/uv
        │   └── linux-arm64/uv
        └── checksums.sha256
```

Treat each `.app`, `.exe`, or `.AppImage` as a **launcher image**, not as the application payload. Generate the images once per product identity and reuse them across application-only releases.

Never embed application source, web assets, dependency manifests, application configuration, API keys, user data, fixed absolute paths, or the changing application version in an image. Embed only the supervisor executable, setup/status UI, wrapper protocol version, icon, and platform metadata.

Rebuild an image only when its supervisor protocol, product display name, product icon, target metadata, or signing changes. Do not rebuild it for changes under `app/src/` or `app/static/`, a new entry module, a dependency-lock change, or a Python-version change supported by the current supervisor protocol.

## Launcher protocol

Copy and customize `assets/m1a-launcher/`. Compile the same standard-library Go supervisor for every target. Make it:

1. derive the release root from its own executable or wrapper path;
2. load `app/launcher/manifest.json`;
3. start an ephemeral HTTP setup/status server on `127.0.0.1`;
4. open the default browser immediately to the status page;
5. choose and integrity-check the bundled `uv` for the running OS/architecture;
6. prepare or reuse the fingerprinted managed runtime;
7. execute `app/launcher/bootstrap.py` with that runtime;
8. wait for the application to publish its effective loopback URL;
9. poll the configured readiness endpoint;
10. redirect the status page to the real GUI only after readiness;
11. supervise the application process until it exits;
12. preserve sanitized logs and return nonzero if the GUI never becomes usable.

Use this schema:

```json
{
  "schema_version": 1,
  "app_id": "com.goosnav.product-name",
  "display_name": "Product Name",
  "python": "3.12.10",
  "entry_module": "product_name.start",
  "ready_path": "/health/ready",
  "startup_timeout_seconds": 180,
  "preferred_port": 0,
  "data_directory_name": "ProductName"
}
```

Validate every field. Require schema version 1, a reverse-DNS-like `app_id`, an exact Python patch version, a Python module entrypoint, a readiness path beginning with `/`, a timeout between 15 and 900 seconds, a port from 0 through 65535, and a single safe data-directory name.

The bootstrap sets these environment variables for the entry module:

```text
GOOSNAV_APP_ROOT
GOOSNAV_APP_DATA
GOOSNAV_CONFIG_DIR
GOOSNAV_DATA_DIR
GOOSNAV_HOST=127.0.0.1
GOOSNAV_PORT_PREFERENCE
GOOSNAV_RUNTIME_STATE
GOOSNAV_LAUNCH_SESSION
```

Require the entry module to bind loopback atomically. Let port `0` request an operating-system-selected free port. Treat a nonzero port as a preference: when it is unavailable, bind port `0` atomically instead of probing and reusing a raced port. After binding and completing mandatory initialization, atomically write `GOOSNAV_RUNTIME_STATE` as:

```json
{"schema_version":1,"pid":12345,"url":"http://127.0.0.1:49152"}
```

Do not make the supervisor probe and release a port before the server binds it. Validate that the reported URL is HTTP and loopback-only before polling or redirecting.

## Operating-system images

### macOS

Generate one universal bundle containing Intel and Apple Silicon supervisor slices:

```text
Open ProductName — macOS.app/
└── Contents/
    ├── Info.plist
    ├── MacOS/launcher
    └── Resources/AppIcon.icns
```

Set `CFBundleExecutable` to `launcher`. Resolve the release root as the parent of the `.app` directory. Do not copy `app/` into the bundle. Keep signing/notarization optional in M1a and mandatory only when the active release requirement says so.

### Windows

Build separate x64 and ARM64 GUI-subsystem executables. Embed the `.ico` resource, suppress a console window, resolve the executable directory with the native process path, and pass explicit argv to children. Never concatenate a shell command from paths or manifest values.

### Linux

Build Type 2 AppImages separately for x86_64 and ARM64. Include `AppRun`, a desktop entry, and PNG icon. Make `AppRun` pass `dirname($APPIMAGE)` as `GOOSNAV_RELEASE_ROOT` before executing the supervisor inside the mounted image. Preserve executable bits in the ZIP. Document the one-time file-manager permission fallback because desktop trust behavior varies.

## Dependency and runtime bootstrap

Bundle a pinned `uv` executable for all six tool targets. Record SHA-256 hashes in `app/launcher/checksums.sha256` and fail with `BOOT-INTEGRITY` on a missing or mismatched tool.

Set the following outside the release root:

```text
UV_PROJECT_ENVIRONMENT=<app-data>/runtimes/<fingerprint>
UV_PYTHON_INSTALL_DIR=<app-data>/python
UV_CACHE_DIR=<app-data>/cache/uv
```

Calculate:

```text
fingerprint = SHA-256(
  schema_version + NUL + os + NUL + architecture + NUL +
  exact_python_version + NUL + pyproject.toml_bytes + NUL + uv.lock_bytes
)
```

Do not include source or static asset bytes in the fingerprint. Put `app/src` first on the bootstrap import path; an editable project installation may provide the same behavior, but must not be required to build on the customer machine. Source edits must take effect on the next launch without rebuilding or resynchronizing the environment.

For a missing ready environment:

1. remove a stale `<fingerprint>.partial` environment;
2. create the environment at `<fingerprint>.partial`;
3. run `uv sync --project <app> --locked --no-dev --managed-python --no-build`;
4. run the bootstrap's bounded validation mode, which imports the entry module without starting the server;
5. write `READY` with the exact fingerprint only after both steps pass;
6. rename the completed partial directory to `<fingerprint>` on the same volume;
7. keep the current and previous ready environments;
8. clean older ready environments only after a successful application start.

Configure `tool.uv.required-environments` for macOS/Windows/Linux on x86_64 and ARM64. Disallow customer-machine source builds. If any production dependency lacks a compatible wheel, change the dependency or reduce the claimed matrix; never ask the customer for a compiler.

Prebuild frontend assets. Do not install Node.js or run a production frontend build on first launch.

After the initial attempt, retry transient dependency downloads at most three times with bounded delays of approximately 1, 2, and 4 seconds. Do not retry integrity, permission, disk-space, invalid lockfile, unsupported platform, or missing-wheel failures automatically.

First launch requires network access unless all managed Python and dependency artifacts are already cached. State this honestly. On offline failure, keep the runtime unready and present a Retry action.

## Process lifecycle and GUI contract

Store platform data beneath:

- macOS: `~/Library/Application Support/<data_directory_name>`;
- Windows: `%LOCALAPPDATA%\<data_directory_name>`;
- Linux: `${XDG_DATA_HOME:-~/.local/share}/<data_directory_name>`.

Separate `cache/`, `config/`, `data/`, `logs/`, `python/`, `runtimes/`, and `runtime/`. Keep source usable from a read-only directory.

Open the setup page before downloads. Show stage, short explanation, log location, error code, and Retry when allowed. Redirect the same tab to the application only after readiness succeeds.

Use an atomic launch lock in application data. When another launcher owns it, validate the recorded instance with the readiness endpoint and reopen the healthy GUI. Never kill a process merely because a port or stale PID is present.

Keep the supervisor as the direct parent of a newly launched application. Capture stdout/stderr in the current log. Handle interrupt and termination signals, request graceful shutdown, wait a bounded interval, then force-kill only the remaining child. Remove owned locks/state on exit.

Closing a browser tab does not prove the server should stop. Let another launcher reopen the healthy instance. Provide an authenticated GUI Quit action that asks the application to shut down cleanly.

If opening the default browser fails, keep the status/application server available, write `OPEN_THIS_URL.txt` beside the current log, and show a native or best-available fallback containing the exact URL. Do not declare M1a accepted until browser opening is verified on the target.

Protect local state-changing endpoints with same-origin checks plus an unguessable per-launch session token or equivalent. The setup server may return its short-lived Retry token to its own same-origin page; never put application credentials, customer secrets, or session tokens in URLs, logs, or error pages.

## Failure contract

Use exactly these stable categories:

| Code | Meaning | Automatic retry |
|---|---|---|
| `LAUNCH-ROOT` | Adjacent `app/` or required launcher files are missing | No |
| `LAUNCH-PLATFORM` | Launcher/tool does not match OS or architecture | No |
| `LAUNCH-BROWSER` | Default browser could not be opened | No |
| `BOOT-INTEGRITY` | Bundled bootstrap tool is missing or corrupt | No |
| `BOOT-NETWORK` | Offline, DNS, proxy, connection, or HTTP failure | Yes, bounded |
| `BOOT-TLS` | Certificate or secure-download failure | Yes, bounded |
| `BOOT-PERMISSION` | Application-data path cannot be written | No |
| `BOOT-DISK` | Insufficient disk space | No |
| `BOOT-LOCK` | Another setup owns the runtime and is not reusable yet | User Retry |
| `DEP-LOCK` | Lockfile is absent, stale, invalid, or incompatible | No |
| `DEP-PLATFORM` | A dependency lacks a supported wheel | No |
| `APP-START` | Application exited before publishing runtime state | User Retry |
| `APP-READY` | Readiness failed or timed out | User Retry |
| `APP-CRASH` | Application exited after becoming ready | User Retry |

Catch Go panics and Python top-level exceptions. Convert them to a stable code, a plain-language summary, and a sanitized log. Do not expose raw tracebacks as the only user output. Preserve previous ready environments and remove only incomplete state owned by the failing launch.

## Packaging and repository rules

Use the committed `assets/m1a-launcher/` template as the canonical launcher source/build definition. Keep product-specific build inputs out of the customer ZIP and customer-facing repository root; retain them in protected build automation or an explicitly private development branch. Keep private plans and agent documents ignored.

Assemble releases from an explicit whitelist. Do not rely on a source-control auto-generated ZIP when it cannot preserve executable modes or required wrapper structure. The packaging job must copy exactly the five images, `README.txt`, `LICENSE.txt`, and `app/`, then verify there are no secrets, private documents, caches, databases, logs, build trees, or user projects.

M1a contains no DRM, activation, login requirement, embedded customer credential, or copy prevention. The sales website controls convenient access. Do not describe unsigned binaries as warning-free: Gatekeeper, SmartScreen, and Linux desktop permissions can still intervene. Move signing, notarization, installers, offline runtime bundling, secure OS credential stores, automatic updates, and optional licensing to M1b.

## Acceptance matrix

Build and exercise:

- Windows x64 and ARM64;
- macOS Intel and Apple Silicon;
- Linux x86_64 and ARM64.

Require evidence for:

1. first launch with no system Python;
2. automatic managed Python and dependency download;
3. setup/status page visible during bootstrap;
4. second launch without unnecessary downloads;
5. source/static edit reflected without an image rebuild;
6. manifest entrypoint edit reflected without an image rebuild;
7. lock/Python edit creating a new environment without an image rebuild;
8. identical launcher-image hashes across application-only updates;
9. paths containing spaces and Unicode;
10. read-only release source;
11. missing `app/`, missing tool, corrupt tool, and corrupt lockfile;
12. offline, DNS, TLS, proxy, disk-full, and permission failures;
13. unavailable binary dependency rejected before release;
14. simultaneous launch and stale/incomplete runtime recovery;
15. port collision and existing-instance reuse;
16. application exit before readiness, readiness timeout, and later crash;
17. browser-open failure and visible fallback URL;
18. restart with preserved application data;
19. graceful GUI quit and forced child cleanup;
20. universal ZIP root whitelist and executable-mode preservation.

Do not mark M1a `CANDIDATE_FOR_ACCEPTANCE` from cross-compilation alone. Require clean target-system GUI smoke evidence for every claimed image.

## Reusable build flow

Customize a copy of `assets/m1a-launcher/project/app/`, replace all manifest/example values, generate a fresh `uv.lock`, and supply product icons as `AppIcon.icns`, `AppIcon.ico`, and `AppIcon.png`.

1. Run `fetch_uv.py --version <exact-uv-version> --app-root <release-root>/app` to download and verify every official archive and generate executable checksums.
2. Run `go test ./...` in `assets/m1a-launcher/supervisor/`.
3. Invoke `build.py` once for each `build_target` in `release-matrix.json`.
4. For Windows, compile `platform/windows/launcher.rc.in` separately for x64 and ARM64 and pass the architecture-matched `.syso` with `--windows-resource`; a Windows image without its product icon fails the build.
5. For Linux, provide `appimagetool` with Type 2 support and run each target on its native architecture for the required smoke evidence.
6. Place the five outputs, customer documents, and `app/` in a staging root. Run `package_universal.py --root <staging-root> --name <display-name> --output <product>.zip`.
7. Compare launcher-image hashes with the prior release whenever only `app/` changed. Any difference is a release failure until explained by an allowed image rebuild reason.

Cross-compilation is useful build evidence, but it never substitutes for the native clean-system acceptance matrix.
