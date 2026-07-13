{{PROJECT_NAME}}

OPEN THE APPLICATION
--------------------
Extract the complete ZIP. Keep every launcher beside the `app` directory.

- macOS: double-click “Open {{PROJECT_NAME}} — macOS.app”.
- Windows x64: double-click “Open {{PROJECT_NAME}} — Windows x64.exe”.
- Windows ARM64: double-click “Open {{PROJECT_NAME}} — Windows ARM64.exe”.
- Linux x86_64: double-click “Open {{PROJECT_NAME}} — Linux x86_64.AppImage”.
- Linux ARM64: double-click “Open {{PROJECT_NAME}} — Linux ARM64.AppImage”.

The first launch opens a setup page and downloads the managed runtime and locked dependencies. No system Python, Node.js, compiler, or terminal command is required. First setup needs network access unless the required files are already cached.

LINUX FIRST-LAUNCH FALLBACK
---------------------------
If the file manager does not launch the AppImage, open its Properties/Permissions and enable “Allow executing file as program,” then double-click it again.

SECURITY PROMPTS
----------------
Unsigned M1a launchers may trigger macOS Gatekeeper or Windows SmartScreen. Replace this section with the exact tested prompt/recovery steps for this release; never promise a warning-free unsigned launch.

RECOVERY
--------
The setup page shows a stable error code, Retry when safe, and the exact log location. Do not move a launcher away from the adjacent `app` directory.

Application data:
Logs:
Support contact:
