#!/usr/bin/env python3
"""Initialize GSPP governance files without overwriting existing project files."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create GSPP governance and planning files in a repository."
    )
    parser.add_argument("--project-root", required=True, help="Repository/project directory")
    parser.add_argument("--name", required=True, help="Human-readable product name")
    parser.add_argument("--slug", help="Repository/product slug; inferred when omitted")
    parser.add_argument("--owner", default="Goosnav LLC", help="Copyright/project owner")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing target files after writing .gspp-backup copies",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    template_root = skill_root / "assets" / "project-templates"
    if not template_root.is_dir():
        print(f"ERROR: Template directory not found: {template_root}", file=sys.stderr)
        return 2

    today = dt.date.today()
    values = {
        "PROJECT_NAME": args.name.strip(),
        "PROJECT_SLUG": args.slug.strip() if args.slug else slugify(args.name),
        "OWNER": args.owner.strip(),
        "DATE": today.isoformat(),
        "DATE_COMPACT": today.strftime("%Y%m%d"),
    }

    created: list[Path] = []
    skipped: list[Path] = []
    overwritten: list[Path] = []

    for source in sorted(template_root.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(template_root)
        target = project_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists() and not args.force:
            skipped.append(relative)
            continue

        if target.exists() and args.force:
            backup = target.with_name(target.name + ".gspp-backup")
            shutil.copy2(target, backup)
            overwritten.append(relative)

        text = source.read_text(encoding="utf-8")
        target.write_text(render(text, values), encoding="utf-8")
        created.append(relative)

    print(f"GSPP initialized at: {project_root}")
    print(f"Created/updated: {len(created)}")
    for path in created:
        print(f"  + {path}")
    if skipped:
        print(f"Preserved existing files: {len(skipped)}")
        for path in skipped:
            print(f"  = {path}")
    if overwritten:
        print("Overwritten files were backed up with the suffix .gspp-backup")

    print("\nNext: complete M0 documents, then set M0 to CANDIDATE_FOR_ACCEPTANCE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
