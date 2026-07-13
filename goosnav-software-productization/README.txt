GOOSNAV SOFTWARE PRODUCTIZATION PROTOCOL (GSPP)
Version 1.1.0

PURPOSE
-------
A portable Agent Skill that defaults to the M1a Universal ZIP: one mutable browser application plus stable native launcher images for macOS, Windows x64/ARM64, and Linux x86_64/ARM64. Later gates add optional signing/offline packaging, CLI/TUI automation, hosted SaaS and a multi-app owner hub/storefront, then mobile clients.

M1a is the first acceptance gate. Planning is its first slice, not a separate blocker. Later implementation waits for explicit user acceptance and continuation.

INSTALLATION
------------
macOS/Linux:

  chmod +x install.sh
  ./install.sh --user

Windows PowerShell:

  Set-ExecutionPolicy -Scope Process Bypass
  .\install.ps1 -Scope User

Repository-scoped installation:

  ./install.sh --repo /path/to/repository

or:

  .\install.ps1 -Scope Repo -RepoPath C:\path\to\repository

The installer replaces one canonical `.agents/skills/goosnav-software-productization` directory and removes same-name legacy copies from `.codex/skills` and `.claude/skills`. Re-running it updates the skill in place rather than creating duplicates.

INITIALIZE A PROJECT
--------------------

  python scripts/init_project.py --project-root /path/to/repo --name "Product Name"

The initializer creates customer README/license placeholders and private M1a planning templates without overwriting existing files. It does not scaffold application code automatically.

M1a LAUNCHER TEMPLATE
---------------------
Read `references/zip-app-architecture.md`, then copy and customize `assets/m1a-launcher/`. It contains:

- a standard-library Go setup/status supervisor and tests;
- a manifest-driven Python bootstrap;
- macOS, Windows, and Linux wrapper metadata;
- a target build script;
- an explicit-whitelist universal ZIP packager.

Launcher images contain no application business logic. Changes under the adjacent `app/` payload do not require rebuilding them.

VALIDATE THE PACKAGE
--------------------

  python scripts/validate_skill.py

Also run the current Agent Skills quick validator. Test the Go supervisor and build every target before using the template in a product release.

COPYRIGHT
---------
Copyright (c) 2026 Goosnav LLC. All rights reserved. See LICENSE.txt.
