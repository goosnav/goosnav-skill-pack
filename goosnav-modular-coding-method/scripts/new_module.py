#!/usr/bin/env python3
"""Scaffold one brick and its testbench.

Dependency-free. Writes a module carrying the full contract header and an
unimplemented entry point, plus a testbench pre-seeded with the four mandatory
case categories. Both are deliberately RED: the testbench fails and
check_module.py reports the stub until the brick is implemented.

    python3 new_module.py --path src/pkg/ledger_parse.py --entry parse_ledger \
        --kind CORE --purpose "Turn raw ledger text into validated transactions."

Language is chosen from the file extension (.py .ts .go .rs). Nothing is
overwritten; an existing path is an error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LANGUAGES = {".py": "python", ".ts": "typescript", ".go": "go", ".rs": "rust"}

HEADER_LINES = [
    "PURPOSE    {purpose}",
    "KIND       {kind}",
    "CONTRACT   IN:  <name: type> -- precondition",
    "           OUT: <type> -- postcondition",
    "           {raises}: <error> when <condition>",
    "GUARANTEES {guarantees}",
    "TUNING     <CONSTANT_NAME> -- range and effect",
    "DECISIONS  D1: chose <X>. Alternative: <Y>. Why not: <Z>.",
    "               Revisit if: <trigger>.",
    "LIMITS     <known unhandled case, explicitly outside the contract>",
    "TESTBENCH  {testbench} -- run with: {command}",
]

PURE_GUARANTEE = "Pure. No I/O, no clock, no randomness. Never mutates its input."
SHELL_GUARANTEE = "Adapter only. Holds no business logic; delegates decisions to CORE bricks."


def header_block(language: str, **values: str) -> str:
    raises = {"python": "RAISES", "typescript": "THROWS"}.get(language, "ERRORS")
    lines = [line.format(raises=raises, **values) for line in HEADER_LINES]
    if language == "python":
        return '"""\n' + "\n".join(lines) + '\n"""'
    if language == "typescript":
        return "/**\n" + "\n".join(f" * {line}" for line in lines) + "\n */"
    prefix = "//! " if language == "rust" else "// "
    return "\n".join(f"{prefix}{line}" for line in lines)


PYTHON_MODULE = '''{header}


def {entry}(value):
    # Not implemented yet. The testbench at {testbench} is RED until it is.
    raise NotImplementedError("{entry} has a contract but no implementation")


if __name__ == "__main__":
    # Demo, not a test. Runs this brick on a representative input so a human can
    # see real output. The gate is {testbench}.
    print({entry}(None))
'''

PYTHON_TEST = '''"""Testbench for {module_import}.{entry} -- run with: {command}

Asserts the contract, not the implementation. Every case below must fail before
the brick exists; a testbench that passes against an unimplemented module is
testing nothing.
"""

import pytest

from {module_import} import {entry}


def test_contract_representative_input():
    """One documented behaviour, representative input, exact expected output."""
    assert {entry}(...) == ...


@pytest.mark.parametrize("value", [...])
def test_boundary_cases(value):
    """Both sides of every boundary named in the preconditions."""
    assert {entry}(value) == ...


def test_error_case():
    """Every entry in the header's error list, asserted to actually raise."""
    with pytest.raises(ValueError):
        {entry}(...)


def test_golden_full_output():
    """One case whose entire expected output is written out and compared verbatim."""
    assert {entry}(...) == ...
'''

TYPESCRIPT_MODULE = '''{header}

import {{ fileURLToPath }} from "node:url";

export function {entry}(value: unknown): unknown {{
  // Not implemented yet. The testbench at {testbench} is RED until it is.
  throw new Error("{entry} has a contract but no implementation");
}}

// Demo, not a test. The gate is {testbench}. fileURLToPath rather than
// new URL(...).pathname: the latter percent-encodes, so the guard silently
// never fires from a path containing a space, and is wrong on Windows.
if (process.argv[1] === fileURLToPath(import.meta.url)) {{
  console.log({entry}(null));
}}
'''

TYPESCRIPT_TEST = '''// Testbench for {entry} -- run with: {command}
// Asserts the contract, not the implementation. Must fail before the brick exists.

import {{ describe, it, expect }} from "vitest";
import {{ {entry} }} from "{module_import}";

describe("{entry}", () => {{
  it("contract: representative input", () => {{
    expect({entry}(null)).toEqual(null);
  }});

  it.each([null])("boundary: %j", (value) => {{
    expect({entry}(value)).toEqual(null);
  }});

  it("error: throws on invalid input", () => {{
    expect(() => {entry}(undefined)).toThrow();
  }});

  it("golden: full output", () => {{
    expect({entry}(null)).toMatchSnapshot();
  }});
}});
'''

GO_MODULE = '''package {package}

import "errors"

{header}
func {entry}(value string) (string, error) {{
	// Not implemented yet. The testbench at {testbench} is RED until it is.
	return "", errors.New("{entry}: not implemented")
}}
'''

GO_TEST = '''package {package}

// Testbench for {entry} -- run with: {command}
// Table-driven; asserts the contract, not the implementation.

import "testing"

func Test{entry}(t *testing.T) {{
	tests := []struct {{
		name    string
		in      string
		want    string
		wantErr bool
	}}{{
		{{name: "contract/representative", in: "", want: "", wantErr: false}},
		{{name: "boundary/empty", in: "", want: "", wantErr: false}},
		{{name: "error/invalid", in: "", want: "", wantErr: true}},
	}}
	for _, tc := range tests {{
		t.Run(tc.name, func(t *testing.T) {{
			got, err := {entry}(tc.in)
			if (err != nil) != tc.wantErr {{
				t.Fatalf("err = %v, wantErr = %v", err, tc.wantErr)
			}}
			if got != tc.want {{
				t.Errorf("got %q, want %q", got, tc.want)
			}}
		}})
	}}
}}
'''

RUST_MODULE = '''{header}

pub fn {entry}(value: &str) -> Result<String, String> {{
    // Not implemented yet. The tests module below is RED until it is.
    todo!("{entry} has a contract but no implementation")
}}

#[cfg(test)]
mod tests {{
    // Testbench -- run with: {command}
    // Exercises the public API only, exactly as an outside caller would.
    use super::*;

    #[test]
    fn contract_representative_input() {{
        assert_eq!({entry}("").unwrap(), "");
    }}

    #[test]
    fn boundary_empty_input() {{
        assert_eq!({entry}("").unwrap(), "");
    }}

    #[test]
    fn error_invalid_input() {{
        assert!({entry}("").is_err());
    }}
}}
'''


def default_testbench(path: Path, language: str) -> Path:
    if language == "python":
        return Path("tests") / f"test_{path.stem}.py"
    if language == "typescript":
        return Path("test") / f"{path.stem}.test.ts"
    if language == "go":
        return path.with_name(f"{path.stem}_test.go")
    return path


def run_command(path: Path, testbench: Path, language: str) -> str:
    if language == "python":
        return f"pytest {testbench} -v"
    if language == "typescript":
        return f"npx vitest run {testbench}"
    if language == "go":
        return f"go test ./{path.parent} -run Test -v"
    return f"cargo test {path.stem}"


def module_import(path: Path, language: str) -> str:
    if language == "python":
        parts = list(path.with_suffix("").parts)
        for root in ("src", "lib"):
            if parts and parts[0] == root:
                parts = parts[1:]
        return ".".join(parts)
    return str(path.with_suffix(""))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scaffold one brick and its testbench.")
    parser.add_argument("--path", required=True, help="module path; extension selects the language")
    parser.add_argument("--entry", required=True, help="public entry point name")
    parser.add_argument("--kind", required=True, choices=["CORE", "SHELL"])
    parser.add_argument("--purpose", required=True, help="one sentence, one verb")
    parser.add_argument("--testbench", help="override the default testbench path")
    args = parser.parse_args(argv[1:])

    path = Path(args.path)
    language = LANGUAGES.get(path.suffix)
    if language is None:
        print(f"ERROR: unsupported extension '{path.suffix}' (use .py .ts .go .rs)", file=sys.stderr)
        return 2
    if path.exists():
        print(f"ERROR: {path} already exists; this script never overwrites", file=sys.stderr)
        return 2

    testbench = Path(args.testbench) if args.testbench else default_testbench(path, language)
    command = run_command(path, testbench, language)
    header = header_block(
        language,
        purpose=args.purpose,
        kind=args.kind,
        guarantees=PURE_GUARANTEE if args.kind == "CORE" else SHELL_GUARANTEE,
        testbench=str(testbench),
        command=command,
    )
    fields = {
        "header": header,
        "entry": args.entry,
        "testbench": str(testbench),
        "command": command,
        "package": path.parent.name or "main",
        "module_import": module_import(path, language),
    }

    templates = {
        "python": (PYTHON_MODULE, PYTHON_TEST),
        "typescript": (TYPESCRIPT_MODULE, TYPESCRIPT_TEST),
        "go": (GO_MODULE, GO_TEST),
        "rust": (RUST_MODULE, None),
    }
    module_template, test_template = templates[language]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(module_template.format(**fields), encoding="utf-8")
    written = [path]
    if test_template is not None:
        if testbench.exists():
            print(f"ERROR: {testbench} already exists; this script never overwrites", file=sys.stderr)
            return 2
        testbench.parent.mkdir(parents=True, exist_ok=True)
        testbench.write_text(test_template.format(**fields), encoding="utf-8")
        written.append(testbench)

    for item in written:
        print(f"Created: {item}")
    print(f"\nStatus: CONTRACTED. Fill in the header's CONTRACT, TUNING, DECISIONS and LIMITS,")
    print(f"then make the testbench fail for the right reason:\n\n    {command}\n")
    print("The brick is RED until implemented. check_module.py will report its stub")
    print("marker until then, which is correct.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
