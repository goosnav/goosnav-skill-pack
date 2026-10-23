#!/usr/bin/env python3
"""Check standalone skill packaging using only the Python standard library."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def local_target(base: Path, value: str) -> None:
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        return
    target = (base / unquote(url.path)).resolve()
    if ROOT not in target.parents and target != ROOT:
        errors.append(f"resource escapes skill: {value}")
    elif not target.is_file():
        errors.append(f"missing resource: {value}")


class ResourceParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("src", "href"):
            if values.get(key):
                local_target(ROOT / "assets", values[key])


required = (
    "SKILL.md", "agents/openai.yaml", "LICENSE.txt", "install.sh", "install.command", "install.ps1",
    "references/pattern-recipes.md", "references/source-and-scope.md",
    "assets/early-web.css", "assets/catalog.html",
)
for filename in required:
    path = ROOT / filename
    if not path.is_file() or not path.stat().st_size:
        errors.append(f"missing or empty file: {filename}")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"\A---\n(.*?)\n---\n", skill, flags=re.S)
metadata = {}
if not match:
    errors.append("SKILL.md must start with closed YAML frontmatter")
else:
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    if metadata.get("name") != ROOT.name:
        errors.append("frontmatter name must match the skill directory")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", metadata.get("name", "")):
        errors.append("name must contain 1-64 lowercase letters, numbers, or hyphens")
    if not 1 <= len(metadata.get("description", "")) <= 1024:
        errors.append("description must contain 1-1024 characters")
    if set(metadata) != {"name", "description"}:
        errors.append("frontmatter must contain only name and description")

for markdown in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
    for link in re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
        local_target(markdown.parent, link)

agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
if "$" + ROOT.name not in agent:
    errors.append("agent default prompt must invoke this skill")
short = re.search(r'\bshort_description:\s*"([^"]+)"', agent)
if not short or not 25 <= len(short.group(1)) <= 64:
    errors.append("agent short description must contain 25-64 characters")

ResourceParser().feed((ROOT / "assets/catalog.html").read_text(encoding="utf-8"))
if len(skill.splitlines()) > 500:
    errors.append("SKILL.md exceeds the 500-line progressive-disclosure limit")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"PASS: {ROOT.name}; metadata, resources, links, and standalone packaging")
