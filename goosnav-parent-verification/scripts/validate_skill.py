#!/usr/bin/env python3
"""Small dependency-free structural check for one Goosnav skill."""
from __future__ import annotations
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent; text = (root / "SKILL.md").read_text(encoding="utf-8"); errors: list[str] = []
if not text.startswith("---\n"): errors.append("SKILL.md frontmatter must start at byte 0")
end = text.find("\n---\n", 4); raw = text[4:end] if end >= 0 else ""; body = text[end + 5:] if end >= 0 else ""; values = {}
for line in raw.splitlines():
    if line and not line[0].isspace() and ":" in line: key, value = line.split(":", 1); values[key] = value.strip()
if values.get("name") != root.name: errors.append("frontmatter name must match the directory")
for key in ("description", "version", "author", "license"):
    if not values.get(key): errors.append(f"missing frontmatter {key}")
for pattern, label in ((r"(?m)^metadata:$", "metadata"), (r"(?m)^  hermes:$", "metadata.hermes"), (r"(?m)^    tags:$", "tags"), (r"(?m)^    related_skills:$", "related_skills")):
    if not re.search(pattern, raw): errors.append(f"missing {label}")
for heading in ("# Overview", "## When to Use", "## Workflow", "## Pitfalls", "## Verification Checklist", "## Exact Recipe"):
    if heading not in body: errors.append(f"missing {heading}")
for path in ("install.sh", "install.ps1"):
    if not (root / path).is_file(): errors.append(f"missing {path}")
if not 5000 <= len(text) <= 13000: errors.append(f"SKILL.md length is {len(text)}, outside target tolerance")
for error in errors: print(f"ERROR: {error}", file=sys.stderr)
if errors: raise SystemExit(1)
print(f"PASS: {root.name} ({len(text)} characters)")
