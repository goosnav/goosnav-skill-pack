#!/usr/bin/env python3
"""Validate all immediate Goosnav Agent Skills without third-party packages."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NEW_SKILLS = {
    "goosnav-mvp-delivery",
    "goosnav-parent-verification",
    "goosnav-local-first-workbench",
    "goosnav-revenue-validation",
    "goosnav-agentic-orchestration",
    "goosnav-research-simulation",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ABSOLUTE_USER_PATH_RE = re.compile(
    r"(?:/Users/(?!<|your/)[^/\s]+|/home/(?!<|your/)[^/\s]+|[A-Za-z]:\\Users\\(?!<|your\\)[^\\\s]+)"
)
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".ps1", ".yaml", ".yml", ".json", ".toml"}


def frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter at byte 0")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    raw = text[4:end]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values, raw, text[end + 5 :]


def run_check(command: list[str], label: str, errors: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        errors.append(f"{label}: {detail or 'command failed'}")


def basic_powershell_check(path: Path, errors: list[str]) -> None:
    """Catch missing entry structure when a real PowerShell parser is unavailable."""
    text = path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^param\(", text):
        errors.append(f"{path.relative_to(ROOT)}: missing top-level param block")
    if '$ErrorActionPreference = "Stop"' not in text:
        errors.append(f"{path.relative_to(ROOT)}: must stop on PowerShell errors")
    for opening, closing, label in (("(", ")", "parentheses"), ("{", "}", "braces")):
        if text.count(opening) != text.count(closing):
            errors.append(f"{path.relative_to(ROOT)}: unbalanced {label} in basic readability check")


def validate_skill(skill: Path, errors: list[str]) -> None:
    name = skill.name
    skill_file = skill / "SKILL.md"
    try:
        text = skill_file.read_text(encoding="utf-8")
        values, raw, body = frontmatter(text)
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{name}: {exc}")
        return

    fm_name = values.get("name", "")
    description = values.get("description", "")
    if fm_name != name or not NAME_RE.fullmatch(fm_name) or len(fm_name) > 64:
        errors.append(f"{name}: frontmatter name must match the valid directory name")
    if not description or len(description) > 1024:
        errors.append(f"{name}: description must contain 1-1024 characters")

    for required in ("install.sh", "install.ps1", "scripts/validate_skill.py"):
        if not (skill / required).is_file():
            errors.append(f"{name}: missing {required}")

    if name in NEW_SKILLS:
        for key in ("version", "author", "license"):
            if not values.get(key):
                errors.append(f"{name}: missing frontmatter {key}")
        if not re.search(r"(?m)^metadata:\s*$", raw) or not re.search(r"(?m)^\s{2}hermes:\s*$", raw):
            errors.append(f"{name}: missing metadata.hermes mapping")
        for key in ("tags", "related_skills"):
            if not re.search(rf"(?m)^\s{{4}}{key}:\s*$", raw):
                errors.append(f"{name}: missing metadata.hermes.{key}")
        for heading in ("# Overview", "## When to Use", "## Workflow", "## Pitfalls", "## Verification Checklist", "## Exact Recipe"):
            if heading not in body:
                errors.append(f"{name}: missing heading {heading}")
        if not 5000 <= len(text) <= 13000:
            errors.append(f"{name}: SKILL.md length {len(text)} is outside the 5-12k target tolerance")

    for installer in (skill / "install.sh", skill / "install.ps1"):
        if installer.is_file() and f'"{name}"' not in installer.read_text(encoding="utf-8"):
            errors.append(f"{name}: {installer.name} does not declare the exact skill name")

    for path in skill.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeError:
                continue
            match = ABSOLUTE_USER_PATH_RE.search(content)
            if match:
                errors.append(f"{name}: absolute user path leakage in {path.relative_to(ROOT)}: {match.group(0)!r}")


def main() -> int:
    errors: list[str] = []
    skills = sorted(path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    names = {path.name for path in skills}
    missing = NEW_SKILLS - names
    if missing:
        errors.append(f"missing required skills: {', '.join(sorted(missing))}")
    if not skills:
        errors.append("no immediate skill directories found")

    for skill in skills:
        validate_skill(skill, errors)
        shell = skill / "install.sh"
        if shell.is_file():
            run_check(["bash", "-n", str(shell)], f"{skill.name}: Bash syntax", errors)
        powershell = skill / "install.ps1"
        if powershell.is_file():
            basic_powershell_check(powershell, errors)

    for required in ("README.md", "install-all.sh", "install-all.ps1"):
        if not (ROOT / required).is_file():
            errors.append(f"pack: missing {required}")
    if (ROOT / "install-all.sh").is_file():
        run_check(["bash", "-n", str(ROOT / "install-all.sh")], "pack: Bash syntax", errors)
    if (ROOT / "install-all.ps1").is_file():
        basic_powershell_check(ROOT / "install-all.ps1", errors)

    pwsh = shutil.which("pwsh")
    if pwsh:
        ps_files = [ROOT / "install-all.ps1", *(skill / "install.ps1" for skill in skills)]
        for path in ps_files:
            if path.is_file():
                escaped = str(path).replace("'", "''")
                command = (
                    "$errors=$null; [System.Management.Automation.Language.Parser]::ParseFile("
                    f"'{escaped}', [ref]$null, [ref]$errors) > $null; "
                    "if ($errors.Count) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }"
                )
                run_check([pwsh, "-NoProfile", "-Command", command], f"{path.name}: PowerShell syntax", errors)
    else:
        print("NOTE: pwsh unavailable; PowerShell files received structural/readability checks only")

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: validated {len(skills)} skills and pack installers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
