#!/usr/bin/env python3
"""Dependency-free structural validation for goosnav-codebase-upgrade."""

from __future__ import annotations

import re
import shutil
# Subprocess is limited to fixed argv with a resolved Bash interpreter.
import subprocess  # nosec B404
import sys
from pathlib import Path


root = Path(__file__).resolve().parent.parent
skill = root / "SKILL.md"
text = skill.read_text(encoding="utf-8")
errors: list[str] = []

if not text.startswith("---\n"):
    errors.append("SKILL.md frontmatter must start at byte 0")
end = text.find("\n---\n", 4)
raw = text[4:end] if end >= 0 else ""
body = text[end + 5 :] if end >= 0 else ""
values: dict[str, str] = {}
for line in raw.splitlines():
    if line and not line[0].isspace() and ":" in line:
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()

if set(values) != {"name", "description"}:
    errors.append("frontmatter must contain only name and description")
if values.get("name") != root.name:
    errors.append("frontmatter name must match the directory")
if not values.get("description") or len(values["description"]) > 1024:
    errors.append("description must contain 1-1024 characters")
for heading in ("# Goosnav Codebase Upgrade", "## Core rules", "## Workflow", "## Pitfalls", "## Verification checklist"):
    if heading not in body:
        errors.append(f"missing heading: {heading}")
for relative in (
    "agents/openai.yaml",
    "install.sh",
    "install.ps1",
    "references/specialist-contracts.md",
    "references/evidence-and-grading.md",
    "scripts/codebase-audit.sh",
    "scripts/summarize-audit.py",
):
    if not (root / relative).is_file():
        errors.append(f"missing {relative}")
for reference in re.findall(r"\]\((references/[^)]+)\)", body):
    if not (root / reference).is_file():
        errors.append(f"broken reference: {reference}")

bash = shutil.which("bash")
if bash:
    # The interpreter is resolved and the checked local path is fixed by this skill.
    shell = subprocess.run(  # nosec B603
        [bash, "-n", str(root / "scripts/codebase-audit.sh")], capture_output=True, text=True
    )
    if shell.returncode:
        errors.append(f"codebase-audit.sh syntax: {shell.stderr.strip()}")
else:
    errors.append("bash is required to validate codebase-audit.sh")
try:
    summary_source = (root / "scripts/summarize-audit.py").read_text(encoding="utf-8")
    compile(summary_source, str(root / "scripts/summarize-audit.py"), "exec")
except (OSError, SyntaxError) as exc:
    errors.append(f"summarize-audit.py syntax: {exc}")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
if errors:
    raise SystemExit(1)
print(f"PASS: {root.name} ({len(text)} characters)")
