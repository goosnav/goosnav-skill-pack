#!/usr/bin/env python3
"""Perform dependency-free structural validation of this Agent Skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_REFS = {
    "references/default-stack.md",
    "references/milestones.md",
    "references/repository-and-docs.md",
    "references/security-and-data.md",
    "references/hosted-saas.md",
    "references/mobile.md",
    "references/testing-and-release.md",
    "references/licensing.md",
    "references/decision-rules.md",
    "references/evals.md",
    "references/zip-app-architecture.md",
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    body = text[end + 5 :]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values, body


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill_file = root / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_file.is_file():
        errors.append("SKILL.md is missing")
    else:
        text = skill_file.read_text(encoding="utf-8")
        try:
            fm, body = parse_frontmatter(text)
            name = fm.get("name", "")
            description = fm.get("description", "")
            if not name:
                errors.append("frontmatter name is missing")
            elif not NAME_RE.fullmatch(name):
                errors.append(f"invalid skill name: {name!r}")
            elif name != root.name:
                errors.append(f"skill name {name!r} must match directory {root.name!r}")
            if not description:
                errors.append("frontmatter description is missing")
            elif len(description) > 1024:
                errors.append("description exceeds 1024 characters")
            if len(name) > 64:
                errors.append("name exceeds 64 characters")
            lines = text.count("\n") + 1
            if lines > 500:
                warnings.append(f"SKILL.md has {lines} lines; Agent Skills recommends under 500")
            if len(body.split()) > 5000:
                warnings.append("SKILL.md body appears to exceed 5000 words/tokens guidance")
        except ValueError as exc:
            errors.append(str(exc))

    for ref in sorted(REQUIRED_REFS):
        if not (root / ref).is_file():
            errors.append(f"missing reference: {ref}")

    for script in ("scripts/init_project.py", "scripts/validate_skill.py"):
        if not (root / script).is_file():
            errors.append(f"missing script: {script}")

    for asset in (
        "assets/m1a-launcher/supervisor/main.go",
        "assets/m1a-launcher/project/app/launcher/bootstrap.py",
        "assets/m1a-launcher/project/app/launcher/manifest.json",
        "assets/m1a-launcher/project/app/launcher/checksums.sha256",
        "assets/m1a-launcher/project/app/pyproject.toml",
        "assets/m1a-launcher/project/app/uv.lock",
        "assets/m1a-launcher/project/app/.python-version",
        "assets/m1a-launcher/project/app/src/.keep",
        "assets/m1a-launcher/project/app/static/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/macos-x64/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/macos-arm64/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/windows-x64/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/windows-arm64/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/linux-x64/.keep",
        "assets/m1a-launcher/project/app/launcher/tools/linux-arm64/.keep",
        "assets/m1a-launcher/build.py",
        "assets/m1a-launcher/fetch_uv.py",
        "assets/m1a-launcher/package_universal.py",
        "assets/m1a-launcher/release-matrix.json",
    ):
        if not (root / asset).is_file():
            errors.append(f"missing launcher asset: {asset}")

    print(f"Skill root: {root}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1
    print("PASS: local structural validation succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
