#!/usr/bin/env python3
"""Dependency-free structural check for a freeform (non-Hermes) skill.

Enforces the essentials the pack relies on: a byte-0 YAML frontmatter whose
`name` matches the directory, a non-empty description, the two installers, and
that every `references/<file>` mentioned in SKILL.md actually exists.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
text = (root / "SKILL.md").read_text(encoding="utf-8")
errors: list[str] = []

if not text.startswith("---\n"):
    errors.append("SKILL.md frontmatter must start at byte 0")
end = text.find("\n---\n", 4)
raw = text[4:end] if end >= 0 else ""
values: dict[str, str] = {}
for line in raw.splitlines():
    if line and not line[0].isspace() and ":" in line:
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

if values.get("name") != root.name:
    errors.append("frontmatter name must match the directory")
description = values.get("description", "")
if not 1 <= len(description) <= 1024:
    errors.append("description must contain 1-1024 characters")

for path in ("install.sh", "install.ps1"):
    if not (root / path).is_file():
        errors.append(f"missing {path}")

# Every references/<name> cited in the body must resolve to a real file.
for ref in sorted(set(re.findall(r"references/([A-Za-z0-9._-]+)", text))):
    if not (root / "references" / ref).is_file():
        errors.append(f"SKILL.md cites references/{ref} but the file is missing")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
if errors:
    raise SystemExit(1)
print(f"PASS: {root.name} ({len(text)} characters)")
