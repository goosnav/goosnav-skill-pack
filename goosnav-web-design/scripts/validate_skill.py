#!/usr/bin/env python3
"""Validate skill metadata, local references, specimen structure, color pairs and converter."""
from __future__ import annotations

from html.parser import HTMLParser
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
    "SKILL.md", "agents/openai.yaml", "LICENSE.txt", "install.sh", "install.command", "install.ps1",
    "references/components.md", "references/sources-and-boundaries.md",
    "assets/goosnav.css", "assets/workbench.html", "assets/workbench.js",
)
for name in required:
    require((ROOT / name).is_file(), f"Missing {name}")
if errors:
    raise SystemExit("\n".join(errors))

skill = (ROOT / "SKILL.md").read_text()
require(skill.startswith("---\n"), "Frontmatter must start at byte 0")
parts = skill.split("---\n", 2)
metadata = dict(re.findall(r"^(name|description): (.+)$", parts[1] if len(parts) == 3 else "", re.M))
require(metadata.get("name") == ROOT.name, "Skill name must match its folder")
require(1 <= len(metadata.get("description", "")) <= 1024, "Description must have 1–1024 characters")
require(len(skill.splitlines()) < 500, "Keep SKILL.md under 500 lines")
require("TODO" not in skill, "Unfinished template in SKILL.md")
for relative in re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill):
    if not relative.startswith(("https://", "http://", "#")):
        require((ROOT / relative.split("#")[0]).is_file(), f"Missing linked resource: {relative}")
agent = (ROOT / "agents/openai.yaml").read_text()
require("$goosnav-web-design" in agent, "Default prompt must invoke the skill")
short = re.search(r'short_description: "(.+)"', agent)
require(bool(short and 25 <= len(short[1]) <= 64), "Short description must have 25–64 characters")


class Specimen(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if attrs.get("id"):
            require(attrs["id"] not in self.ids, f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for attr in ("for", "aria-labelledby", "aria-describedby"):
            self.targets.extend((attrs.get(attr) or "").split())
        for attr in ("src", "href"):
            value = attrs.get(attr) or ""
            if value.startswith("#"):
                self.targets.append(value[1:])
            elif value:
                require(not value.startswith(("http:", "https:", "//")), "Specimen must work without external assets")
                require((ROOT / "assets" / value).is_file(), f"Missing specimen asset: {value}")


html = (ROOT / "assets/workbench.html").read_text()
parser = Specimen()
parser.feed(html)
for target in parser.targets:
    require(target in parser.ids, f"Missing HTML label/anchor target: {target}")
require(html.count("<h1 ") == 1, "Specimen must have one H1")
require('role="status"' in html and 'role="alert"' in html, "Missing status/error announcement regions")
css = (ROOT / "assets/goosnav.css").read_text()
require("prefers-reduced-motion" in css and ":focus-visible" in css, "Missing motion/focus treatment")
require("@import" not in css and "@font-face" not in css, "Starter CSS must have no external font dependency")
tokens = dict(re.findall(r"(--gn-[\w-]+):\s*([^;]+);", css))


def luminance(token: str) -> float:
    value = tokens.get(token, token)
    while value.startswith("var("):
        value = tokens[value[4:-1]]
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    channels = [int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))


for foreground, background in (
    ("--gn-ink", "--gn-paper"), ("--gn-muted", "--gn-paper"),
    ("--gn-blue", "--gn-paper"), ("--gn-error", "--gn-paper"),
    ("--gn-success", "--gn-paper"), ("--gn-ink", "--gn-yellow"),
    ("#ffffff", "--gn-action"),
    ("#ffffff", "--gn-action-hover"), ("#606060", "#eeeeee"),
):
    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    require((light + .05) / (dark + .05) >= 4.5, f"Insufficient text contrast: {foreground} on {background}")

node = shutil.which("node")
if node:
    js = ROOT / "assets/workbench.js"
    syntax = subprocess.run([node, "--check", str(js)], text=True, capture_output=True)
    require(syntax.returncode == 0, syntax.stderr or "JavaScript syntax failed")
    checks = r'''
const assert = require("node:assert/strict");
const { convertList } = require(process.argv[1]);
assert.deepEqual(convertList(" Alpha \r\n\nBeta\rAlpha ").items, ["Alpha", "Beta"]);
assert.deepEqual(convertList("Beta\nAlpha\nBeta", {deduplicate:false, sort:true}).items, ["Alpha", "Beta", "Beta"]);
const result = convertList('"quoted"\n<script>alert(1)</script>\ncafé\n猫');
assert.deepEqual(JSON.parse(result.json), ['"quoted"', '<script>alert(1)</script>', 'café', '猫']);
assert.equal(result.bytes, new TextEncoder().encode(result.json).byteLength);
assert.deepEqual(convertList("\uFEFFsample").items, ["sample"]);
assert.throws(() => convertList(" \n\t"), /nonempty/);
assert.throws(() => convertList("binary\u0000file"), /binary/);
assert.throws(() => convertList("x".repeat(1001)), /1,000/);
assert.throws(() => convertList("x\n".repeat(5001)), /5,000/);
assert.throws(() => convertList("x".repeat(262145)), /256 KiB/);
console.log("PASS: converter input, escaping, UTF-8, options, and failure boundaries");
'''
    result = subprocess.run([node, "-e", checks, str(js)], text=True, capture_output=True)
    require(result.returncode == 0, result.stderr or "Converter behavior failed")
    if result.returncode == 0:
        print(result.stdout.strip())
else:
    print("NOTE: Node unavailable; converter behavior was not exercised.")

for error in errors:
    print(f"ERROR: {error}", file=sys.stderr)
if errors:
    raise SystemExit(1)
print(f"PASS: {ROOT.name} metadata, references, specimen structure, and color pairs")
