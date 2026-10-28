#!/usr/bin/env python3
"""Dependency-free checks for the heartbeat skill's installable resources."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


required = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/prompt-template.md",
    "install.sh",
    "install.command",
    "install.ps1",
)
for relative in required:
    require((ROOT / relative).is_file(), f"Missing {relative}")
if errors:
    raise SystemExit("\n".join(errors))

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
require(frontmatter is not None, "SKILL.md must start with closed YAML frontmatter")
metadata = {}
if frontmatter:
    for line in frontmatter[1].splitlines():
        key, separator, value = line.partition(":")
        require(bool(separator and key and not key[0].isspace()), "Use scalar frontmatter fields")
        require(key not in metadata, f"Duplicate frontmatter field: {key}")
        metadata[key] = value.strip().strip('"').strip("'")
require(set(metadata) == {"name", "description"}, "Frontmatter must contain only name and description")
require(metadata.get("name") == ROOT.name, "Skill name must match its folder")
require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata.get("name", ""))), "Invalid skill name")
require(len(metadata.get("name", "")) <= 64, "Skill name must not exceed 64 characters")
require(1 <= len(metadata.get("description", "")) <= 1024, "Description must have 1–1024 characters")
require(len(skill.splitlines()) < 500, "Keep SKILL.md under 500 lines")

template = (ROOT / "references/prompt-template.md").read_text(encoding="utf-8")
for path, content in ((ROOT / "SKILL.md", skill), (ROOT / "references/prompt-template.md", template)):
    for relative in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", relative) or relative.startswith("#"):
            continue
        target = (path.parent / relative.split("#")[0]).resolve()
        require(target.is_relative_to(ROOT), f"Resource escapes skill directory: {relative}")
        require(target.is_file(), f"Missing linked resource: {relative}")
require("references/prompt-template.md" in skill, "SKILL.md must link the prompt template")

# These section names are the scratchpad's interface, not wording requirements
# for the surrounding instructions. Headings may use any Markdown depth.
headings = {heading.strip().casefold() for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", template, re.M)}
for heading in (
    "Current objective", "Sources to use", "Current state",
    "Ranked candidates / hypotheses / tasks", "Deprioritized items",
    "Next actions", "Guardrails", "Stop condition",
):
    require(heading.casefold() in headings, f"Prompt template missing section: {heading}")

agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
require(bool(re.search(r"(?m)^interface:\s*$", agent)), "Missing interface metadata")
interface = {}
for key in ("display_name", "short_description", "default_prompt"):
    match = re.search(rf'^  {key}: (".*")$', agent, re.M)
    require(match is not None, f"Missing quoted interface.{key}")
    if match:
        try:
            interface[key] = json.loads(match[1])
        except json.JSONDecodeError:
            errors.append(f"Invalid quoted interface.{key}")
require(bool(interface.get("display_name", "").strip()), "Display name must not be empty")
require(25 <= len(interface.get("short_description", "")) <= 64, "Short description must have 25–64 characters")
require(f"${ROOT.name}" in interface.get("default_prompt", ""), "Default prompt must invoke this skill")

for relative in ("install.sh", "install.ps1"):
    content = (ROOT / relative).read_text(encoding="utf-8")
    require(f'"{ROOT.name}"' in content, f"{relative} must declare the exact skill name")
bash = shutil.which("bash")
if bash:
    for relative in ("install.sh", "install.command"):
        result = subprocess.run([bash, "-n", str(ROOT / relative)], capture_output=True, text=True)
        require(result.returncode == 0, f"{relative} syntax: {result.stderr.strip()}")
else:
    print("NOTE: Bash unavailable; shell syntax was not checked")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
if errors:
    raise SystemExit(1)
print(f"PASS: {ROOT.name} metadata, scratchpad template, local references, and installers")
