#!/usr/bin/env python3
"""Check one brick against the Goosnav Modular Coding Method.

Dependency-free. Verifies the contract header, the sibling testbench, the size
and entry-point limits, CORE purity, and the absence of stub markers.

    python3 check_module.py <path-to-module> [<path-to-module> ...]

Exit code 0 when every brick passes, 1 when any brick fails. A freshly
scaffolded brick is expected to FAIL on its stub marker until it is implemented;
that is the RED state, not a defect in this checker.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = (
    "PURPOSE",
    "KIND",
    "CONTRACT",
    "GUARANTEES",
    "TUNING",
    "DECISIONS",
    "LIMITS",
    "TESTBENCH",
)

SOFT_LINES = 200
HARD_LINES = 300
MAX_ENTRY_POINTS = 3

LANGUAGES = {".py": "python", ".ts": "typescript", ".tsx": "typescript",
             ".js": "typescript", ".mjs": "typescript", ".go": "go", ".rs": "rust"}

# Leading tokens stripped from a header line before looking for a field label.
COMMENT_TOKENS = ("//!", "///", "//", "#!", "#", "/**", "/*", "*/", "*",
                  '"""', "'''", "!")

# Where the demo or in-file test block starts. Lines from here on are excluded
# from the implementation line count: a demo and a testbench are not payload.
TAIL_MARKERS = {
    "python": (re.compile(r"^if\s+__name__\s*==")),
    "typescript": re.compile(r"^if\s*\(\s*(?:process\.argv\[1\]|require\.main)"),
    "rust": re.compile(r"^#\[cfg\(test\)\]"),
    "go": None,
}

# CORE bricks may not reach the outside world. Import names are matched against
# the module actually imported; call patterns catch the impurity that arrives
# without an import (a method on an already-imported module).
FORBIDDEN_IMPORTS = {
    "python": {"os", "sys", "pathlib", "subprocess", "socket", "shutil", "tempfile",
               "sqlite3", "random", "secrets", "requests", "httpx", "urllib",
               "urllib.request", "http", "boto3", "psycopg2", "pymongo", "redis"},
    "typescript": {"node:fs", "fs", "node:net", "net", "node:http", "http",
                   "node:https", "https", "node:child_process", "child_process",
                   "node:crypto", "crypto", "node:dns", "node:os", "axios"},
    "go": {"os", "io", "io/ioutil", "net", "net/http", "database/sql",
           "math/rand", "os/exec", "bufio"},
    "rust": {"std::fs", "std::net", "std::process", "std::env", "rand",
             "reqwest", "tokio::fs", "tokio::net"},
}

FORBIDDEN_CALLS = {
    "python": (r"\bopen\s*\(", r"\bos\.environ", r"\bdatetime\.now\s*\(",
               r"\bdatetime\.today\s*\(", r"\btime\.time\s*\(", r"\brandom\."),
    "typescript": (r"\bfetch\s*\(", r"\bDate\.now\s*\(", r"\bnew Date\s*\(\s*\)",
                   r"\bMath\.random\s*\(", r"\bprocess\.env\b"),
    "go": (r"\btime\.Now\s*\(", r"\brand\.", r"\bos\.Getenv\s*\("),
    "rust": (r"\bSystemTime::now\s*\(", r"\bInstant::now\s*\(", r"\benv::var\s*\("),
}

STUB_MARKERS = (
    (re.compile(r"\bTODO\b"), "TODO marker"),
    (re.compile(r"\bFIXME\b"), "FIXME marker"),
    (re.compile(r"\bXXX\b"), "XXX marker"),
    (re.compile(r"\bNotImplementedError\b"), "NotImplementedError stub"),
    (re.compile(r"\btodo!\s*\("), "todo!() stub"),
    (re.compile(r"\bunimplemented!\s*\("), "unimplemented!() stub"),
    (re.compile(r"not\s+implemented", re.IGNORECASE), "'not implemented' stub"),
)

ENTRY_POINT_PATTERNS = {
    "typescript": re.compile(r"^export\s+(?:async\s+)?(?:function|class|const\s+\w+\s*=\s*(?:async\s*)?\()"),
    "go": re.compile(r"^func\s+[A-Z]"),
    "rust": re.compile(r"^pub\s+(?:async\s+)?fn\s"),
}

TESTBENCH_GLOBS = {
    "python": ("test_{stem}.py", "{stem}_test.py"),
    "typescript": ("{stem}.test.ts", "{stem}.spec.ts", "{stem}.test.js", "{stem}.spec.js"),
    "go": ("{stem}_test.go",),
    "rust": (),  # Rust keeps unit tests in-file; handled separately.
}


def strip_comment_tokens(line: str) -> str:
    """Remove leading comment punctuation so a field label can be matched."""
    text = line.strip()
    changed = True
    while changed:
        changed = False
        for token in COMMENT_TOKENS:
            if text.startswith(token):
                text = text[len(token):].strip()
                changed = True
    return text


def read_header(lines: list[str]) -> tuple[dict[str, str], int]:
    """Return the header fields and the line index where the header ends.

    The header is searched in the first 150 lines rather than by locating the
    exact comment block, because four languages express that block four ways and
    the field labels are unambiguous on their own.
    """
    fields: dict[str, str] = {}
    last = 0
    current: str | None = None
    for index, raw in enumerate(lines[:150]):
        text = strip_comment_tokens(raw)
        match = re.match(r"^([A-Z]{4,10})\s\s*(.*)$", text)
        if match and match.group(1) in REQUIRED_FIELDS:
            current = match.group(1)
            fields[current] = match.group(2).strip()
            last = index
        elif current and text and not re.match(r"^[A-Z]{4,10}\s", text):
            # Continuation of a wrapped field such as CONTRACT or DECISIONS.
            fields[current] += "\n" + text
            last = index
        elif not text:
            current = None
    return fields, last


def find_testbench(path: Path, language: str, declared: str) -> Path | None:
    """Locate the sibling testbench, preferring the path the header declares."""
    # The declared path is everything before the " -- run with:" suffix. A field
    # that carries no path at all falls through to the name-based search.
    words = declared.split("--")[0].strip().split()
    if words:
        candidate_text = words[0]
        for base in (Path.cwd(), path.parent, *path.parents):
            candidate = base / candidate_text
            if candidate.is_file():
                return candidate
    names = [pattern.format(stem=path.stem) for pattern in TESTBENCH_GLOBS[language]]
    if not names:
        return None
    roots = [path.parent, *list(path.parents)[:4]]
    for root in roots:
        for name in names:
            direct = root / name
            if direct.is_file():
                return direct
        for sub in ("tests", "test", "__tests__", "spec"):
            folder = root / sub
            if folder.is_dir():
                for name in names:
                    found = next(folder.rglob(name), None)
                    if found:
                        return found
    return None


def count_implementation_lines(lines: list[str], language: str, header_end: int) -> int:
    """Count payload lines: not blank, not comment, not header, not demo, not tests."""
    marker = TAIL_MARKERS[language]
    total = 0
    for raw in lines[header_end + 1:]:
        text = raw.strip()
        if marker is not None and marker.match(text):
            break
        if not text:
            continue
        if any(text.startswith(token) for token in ("//", "#", "/*", "*", '"""', "'''")):
            continue
        total += 1
    return total


def python_entry_points(source: str) -> list[str] | None:
    """Public module-level functions and classes, via the real parser."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    names = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
    return names


def python_imports(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return found


def textual_imports(lines: list[str], language: str) -> set[str]:
    found: set[str] = set()
    for raw in lines:
        text = raw.strip()
        if language == "typescript":
            match = re.search(r"""(?:from|require\()\s*['"]([^'"]+)['"]""", text)
            if match:
                found.add(match.group(1))
        elif language == "go":
            match = re.match(r'^(?:\w+\s+)?"([^"]+)"$', text) or re.match(r'^import\s+"([^"]+)"', text)
            if match:
                found.add(match.group(1))
        elif language == "rust":
            match = re.match(r"^use\s+([A-Za-z0-9_:]+)", text)
            if match:
                found.add("::".join(match.group(1).split("::")[:2]))
    return found


def check(path: Path) -> list[str]:
    problems: list[str] = []
    language = LANGUAGES.get(path.suffix)
    if language is None:
        return [f"unsupported file type '{path.suffix}' (expected .py .ts .js .go .rs)"]

    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    fields, header_end = read_header(lines)

    for field in REQUIRED_FIELDS:
        if field not in fields:
            problems.append(f"header is missing {field}")
        elif not fields[field].strip():
            problems.append(f"header field {field} is empty")

    kind = fields.get("KIND", "").strip().upper()
    if kind not in {"CORE", "SHELL"}:
        problems.append(f"KIND must be CORE or SHELL, found '{fields.get('KIND', '')}'")

    purpose = fields.get("PURPOSE", "")
    if purpose.count(".") > 1 or " and " in purpose.lower():
        problems.append("PURPOSE reads as more than one responsibility; consider splitting the brick")

    decisions = fields.get("DECISIONS", "")
    if decisions and decisions.strip().lower() not in {"none", "none.", "n/a"}:
        if not re.search(r"\bD\d+:", decisions):
            problems.append("DECISIONS has no numbered entry (D1:, D2:, ...)")
        if "alternative" not in decisions.lower():
            problems.append("DECISIONS names no alternative considered")
        if "revisit if" not in decisions.lower():
            problems.append("DECISIONS has no 'Revisit if:' trigger")

    if language == "rust":
        if "#[cfg(test)]" not in source:
            problems.append("no #[cfg(test)] test module in this file")
    else:
        testbench = find_testbench(path, language, fields.get("TESTBENCH", ""))
        if testbench is None:
            problems.append("no sibling testbench found; TESTBENCH must name a file that exists")

    implementation_lines = count_implementation_lines(lines, language, header_end)
    if implementation_lines > HARD_LINES:
        problems.append(f"{implementation_lines} implementation lines exceeds the hard cap of {HARD_LINES}; re-split this brick")
    elif implementation_lines > SOFT_LINES:
        problems.append(f"WARN {implementation_lines} implementation lines exceeds the soft cap of {SOFT_LINES}")

    if language == "python":
        entry_points = python_entry_points(source)
        if entry_points is None:
            problems.append("file does not parse as Python")
            entry_points = []
    else:
        pattern = ENTRY_POINT_PATTERNS[language]
        entry_points = [line for line in lines if pattern.match(line.strip())]
    if len(entry_points) > MAX_ENTRY_POINTS:
        problems.append(f"{len(entry_points)} public entry points exceeds the maximum of {MAX_ENTRY_POINTS}")

    if kind == "CORE":
        imports = python_imports(source) if language == "python" else textual_imports(lines, language)
        for banned in sorted(FORBIDDEN_IMPORTS[language] & imports):
            problems.append(f"CORE brick imports '{banned}'; move that I/O to a SHELL brick")
        marker = TAIL_MARKERS[language]
        body: list[str] = []
        for raw in lines[header_end + 1:]:
            if marker is not None and marker.match(raw.strip()):
                break   # the demo block may touch the outside world; the brick may not
            body.append(raw)
        for pattern in FORBIDDEN_CALLS[language]:
            for raw in body:
                text = raw.strip()
                if text.startswith(("#", "//", "*", "///")):
                    continue
                if re.search(pattern, text):
                    problems.append(f"CORE brick is not pure: matches {pattern} at '{text[:60]}'")
                    break

    for pattern, label in STUB_MARKERS:
        if pattern.search(source):
            problems.append(f"{label} present; a brick with a stub is not GREEN")

    return problems


def main(argv: list[str]) -> int:
    paths = [Path(arg) for arg in argv[1:]]
    if not paths:
        print(__doc__, file=sys.stderr)
        return 2

    failed = 0
    for path in paths:
        if not path.is_file():
            print(f"FAIL: {path}\n  - file not found", file=sys.stderr)
            failed += 1
            continue
        problems = check(path)
        hard = [item for item in problems if not item.startswith("WARN ")]
        warnings = [item for item in problems if item.startswith("WARN ")]
        if hard:
            failed += 1
            print(f"FAIL: {path}", file=sys.stderr)
            for item in hard:
                print(f"  - {item}", file=sys.stderr)
            for item in warnings:
                print(f"  ~ {item[5:]}", file=sys.stderr)
        else:
            for item in warnings:
                print(f"WARN: {path}\n  ~ {item[5:]}", file=sys.stderr)
            print(f"PASS: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
