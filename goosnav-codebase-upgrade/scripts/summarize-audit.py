#!/usr/bin/env python3
"""Summarize one fresh codebase-audit run without third-party packages."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


GRADE_RE = re.compile(r"^\s*(?P<item>.+?)\s+-\s+(?P<grade>[C-F])\s+\((?P<score>\d+)\)\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: summarize-audit.py RUN_DIRECTORY", file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1]).resolve()
    status_path = run_dir / "status.tsv"
    if not status_path.is_file():
        print(f"Missing status manifest: {status_path}", file=sys.stderr)
        return 2

    with status_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    counts = Counter(row["status"] for row in rows)

    hotspots: list[tuple[str, int, str]] = []
    radon_log = run_dir / "21-radon-cc-c-f.txt"
    if radon_log.is_file():
        for line in radon_log.read_text(encoding="utf-8", errors="replace").splitlines():
            match = GRADE_RE.match(line)
            if match:
                hotspots.append((match["grade"], int(match["score"]), match["item"].strip()))
    hotspots.sort(key=lambda item: (-item[1], item[2]))

    lines = [
        "# Codebase audit summary",
        "",
        "> This is triage evidence, not a release verdict. Skipped checks are unverified,",
        "> scanner findings require semantic review, and passing tools do not prove user workflows.",
        "",
        "## Check status",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status in ("PASS", "FINDINGS", "FAIL", "ERROR", "SKIPPED"):
        lines.append(f"| {status} | {counts.get(status, 0)} |")

    lines.extend(["", "## Checks requiring attention", ""])
    attention = [row for row in rows if row["status"] in {"FINDINGS", "FAIL", "ERROR"}]
    if attention:
        for row in attention:
            lines.append(f"- `{row['id']}`: {row['status']} (exit {row['exit_code']}); inspect `{Path(row['log']).name}`.")
    else:
        lines.append("- No executed check returned findings, failure, or error.")

    lines.extend(["", "## Unverified coverage", ""])
    skipped = [row for row in rows if row["status"] == "SKIPPED"]
    if skipped:
        for row in skipped:
            lines.append(f"- `{row['id']}`: {row['command']}")
    else:
        lines.append("- No checks were skipped.")

    lines.extend(["", "## Complexity hotspots requiring disposition", ""])
    if hotspots:
        lines.append("Every D/E/F item requires semantic review. Review C when it touches a primary user journey, trust/data boundary, high-churn code, or weak tests.")
        lines.extend(["", "| Grade | Score | Symbol |", "| --- | ---: | --- |"])
        for grade, score, item in hotspots:
            lines.append(f"| {grade} | {score} | {item.replace('|', '\\|')} |")
    else:
        lines.append("- No C–F Radon function result was recorded; this may mean none exist or Radon was skipped/errored.")

    lines.extend(
        [
            "",
            "## Required human follow-up",
            "",
            "- Link findings to reachable code, user harm, security/data risk, tests, and the accepted user journey.",
            "- Rerun important checks directly with repository-native commands and preserve their real exit codes.",
            "- Launch the documented product and exercise happy, failure, persistence/reopen, and export paths.",
            "- Review screenshots with browser console/network evidence; appearance alone does not prove function.",
            "- Treat dependency and secret scans as leads, not security guarantees.",
        ]
    )
    output = run_dir / "summary.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
