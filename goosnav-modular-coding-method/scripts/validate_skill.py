#!/usr/bin/env python3
"""Dependency-free structural validation for goosnav-modular-coding-method."""

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
for heading in (
    "# Goosnav Modular Coding Method",
    "## Core rules",
    "## Operating modes",
    "## Workflow",
    "## Pitfalls",
    "## Verification checklist",
    "## Reference loading map",
):
    if heading not in body:
        errors.append(f"missing heading: {heading}")
for relative in (
    "agents/openai.yaml",
    "install.sh",
    "install.ps1",
    "LICENSE.txt",
    "references/module-contract.md",
    "references/testbench.md",
    "references/module-map.md",
    "references/carve-out.md",
    "references/language-python.md",
    "references/language-typescript.md",
    "references/language-go.md",
    "references/language-rust.md",
    "references/method-lineage.md",
    "scripts/check_module.py",
    "scripts/new_module.py",
):
    if not (root / relative).is_file():
        errors.append(f"missing {relative}")
for reference in re.findall(r"\]\((references/[^)]+)\)", body):
    if not (root / reference).is_file():
        errors.append(f"broken reference: {reference}")

# Every reference file must be reachable from SKILL.md, or it is dead weight.
for candidate in sorted((root / "references").glob("*.md")):
    if f"references/{candidate.name}" not in body:
        errors.append(f"unreferenced file: references/{candidate.name}")

# The four mandatory header fields must appear in the skill and in the contract
# reference, so the two cannot drift apart.
contract_text = (root / "references/module-contract.md").read_text(encoding="utf-8")
for field in ("PURPOSE", "KIND", "CONTRACT", "GUARANTEES", "TUNING", "DECISIONS", "LIMITS", "TESTBENCH"):
    if field not in body:
        errors.append(f"SKILL.md omits header field: {field}")
    if field not in contract_text:
        errors.append(f"module-contract.md omits header field: {field}")

for script in ("scripts/check_module.py", "scripts/new_module.py"):
    try:
        source = (root / script).read_text(encoding="utf-8")
        compile(source, str(root / script), "exec")
    except (OSError, SyntaxError) as exc:
        errors.append(f"{script} syntax: {exc}")

bash = shutil.which("bash")
if bash:
    # The interpreter is resolved and the checked local path is fixed by this skill.
    shell = subprocess.run(  # nosec B603
        [bash, "-n", str(root / "install.sh")], capture_output=True, text=True
    )
    if shell.returncode:
        errors.append(f"install.sh syntax: {shell.stderr.strip()}")
else:
    errors.append("bash is required to validate install.sh")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
if errors:
    raise SystemExit(1)
print(f"PASS: {root.name} ({len(text)} characters)")
