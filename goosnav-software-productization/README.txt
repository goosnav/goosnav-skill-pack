GOOSNAV SOFTWARE PRODUCTIZATION PROTOCOL (GSPP)
Version 1.0.0

PURPOSE
-------
A portable Agent Skill for Claude Code, Codex, and other clients that implement the open Agent Skills format. It directs coding agents to build software through gated commercial milestones:

M0  Product contract and architecture
M1a Local browser application, sellable Zip Edition (launchers + first-run wizard)
M1b Packaged desktop edition (Tauri + bundled runtime), deferrable polish upgrade
M2  CLI + optional TUI automation surfaces
M3  Hosted subscription SaaS + owner command center
M4  iOS + Android applications

The skill plans the entire path but allows implementation only in the active milestone. Each milestone stops at CANDIDATE_FOR_ACCEPTANCE until the user approves it.

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

Manual personal installation:

  Claude Code: copy this folder to ~/.claude/skills/goosnav-software-productization
  Codex:       copy this folder to ~/.codex/skills/goosnav-software-productization
  Shared:      ~/.agents/skills/goosnav-software-productization for other Agent Skills clients

Claude Code invokes it explicitly as:

  /goosnav-software-productization

Codex invokes it explicitly as:

  $goosnav-software-productization

Both clients may also activate it automatically when a request matches the skill description.

INITIALIZE A PROJECT
--------------------
The agent can run:

  python scripts/init_project.py --project-root /path/to/repo --name "Product Name"

The initializer creates governance and planning templates without overwriting existing files. It does not scaffold application code.

VALIDATE THE PACKAGE
--------------------

  python scripts/validate_skill.py

This performs local structural checks. For formal Agent Skills validation, use the current official skills-ref validator when available.

DESIGN POSITION
---------------
The architecture is a ports-and-adapters productization ladder. A shared domain/application core is exposed through thin browser, desktop, CLI, TUI, hosted, admin, and mobile adapters. The frontend is simple-first: plain HTML/CSS/JS served by the backend, with React reserved for genuinely complex UIs.

The protocol deliberately rejects two fragile patterns:

1. requiring end users to perform manual environment setup — the M1a Zip Edition bootstraps its own dependencies through an automatic first-run wizard, and the M1b Packaged Edition bundles the runtime entirely;
2. storing production or hosted secrets in a project .env file.

COPYRIGHT
---------
Copyright (c) 2026 Goosnav LLC. All rights reserved. See LICENSE.txt.
