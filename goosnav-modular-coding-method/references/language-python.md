# Python recipe

## Layout

```text
src/<package>/
    ledger_parse.py           # the brick
    money_round.py
tests/
    test_ledger_parse.py      # the testbench
    assembly/
        test_rung_02.py       # seam tests, cumulative
fixtures/
    ledger_parse/golden_basic.json
```

Keep the testbench in `tests/` mirroring the module path, which is what pytest discovery and most repositories already expect. If the project instead keeps tests beside sources, follow the project.

## Header

Module docstring, first statement in the file, before imports.

```python
"""
PURPOSE    Turn raw ledger text into validated transactions.
KIND       CORE
CONTRACT   IN:  raw: str -- UTF-8 text, may be empty
           OUT: list[Transaction] -- source order preserved, may be empty
           RAISES: LedgerFormatError when a non-blank line has fewer than 3 fields
GUARANTEES Pure. No I/O, no clock, no randomness. Never mutates its input.
TUNING     FIELD_SEPARATOR, MAX_LINE_BYTES
DECISIONS  D1: chose line-at-a-time parsing. Alternative: regex over the whole
               text. Why not: regex loses the line number needed for the error
               message. Revisit if: error messages stop needing line numbers.
LIMITS     Assumes UTF-8. Does not handle quoted separators inside fields.
TESTBENCH  tests/test_ledger_parse.py -- run with: pytest tests/test_ledger_parse.py -v
"""
```

## Contract expression

Type hints on the entry point, always. For boundary types use a frozen dataclass rather than a dict or a tuple -- a named type at the boundary is what makes the contract real:

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Transaction:
    identifier: str
    cents: int
    posted_on: date
```

`TypedDict` where the data must stay a dict for serialization. `NamedTuple` for small positional values. Enforce preconditions in `CORE` bricks with plain `assert` or an explicit raise at the top of the entry point; the contract says who is responsible, and a violated precondition is a caller bug that should be loud.

Use pydantic only in `SHELL` bricks, at the process edge, where untrusted data arrives. Do not pull a validation library into pure logic that already has types.

## Purity

A `CORE` brick must not import `os`, `sys`, `pathlib`, `open`, `requests`, `httpx`, `socket`, `subprocess`, `sqlite3`, `random`, `time`, `datetime.now`, or read `os.environ`. Pass a timestamp, a seed, or loaded config in as an argument; the calling `SHELL` brick owns the impurity.

## Testbench

```python
import pytest
from mypackage.ledger_parse import parse_ledger, LedgerFormatError

def test_contract_parses_two_transactions():        # contract case
    ...

@pytest.mark.parametrize("raw", ["", "\n", "   \n\n"])
def test_boundary_blank_input_yields_empty(raw):    # boundary cases
    assert parse_ledger(raw) == []

def test_raises_on_short_line():                    # error case
    with pytest.raises(LedgerFormatError, match="line 2"):
        parse_ledger("a|1|2024-01-01\nbad")

def test_golden_basic(golden):                      # golden case
    ...
```

Run one testbench: `pytest tests/test_ledger_parse.py -v`. Run one case: `pytest tests/test_ledger_parse.py::test_raises_on_short_line -v`.

**Properties** with Hypothesis, for `CORE` bricks:

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_never_raises_unexpected_type(raw):
    try:
        parse_ledger(raw)
    except LedgerFormatError:
        pass    # documented in RAISES; anything else fails the property
```

**Goldens** with a fixture file compared verbatim, or `syrupy` (`assert result == snapshot`) if the project already uses it. Regenerate a golden only as a deliberate, explained change.

**Shell bricks:** contract-tested against `tmp_path`, a fake client, or `monkeypatch`; plus exactly one test hitting the real resource, marked so it can be selected or skipped (`@pytest.mark.smoke`).

## Demo entry point

```python
if __name__ == "__main__":
    # Demo, not a test. Runs this brick on a representative input so a human
    # can see real output. The gate is tests/test_ledger_parse.py.
    sample = "acct-1|1250|2024-01-01\nacct-2|-300|2024-01-02"
    for transaction in parse_ledger(sample):
        print(transaction)
```

Run it with `python -m mypackage.ledger_parse` so imports resolve the same way they do in production. `python src/mypackage/ledger_parse.py` will break relative imports and is not the supported command.

## Commands to cite as evidence

```bash
pytest tests/test_ledger_parse.py -v
python -m mypackage.ledger_parse
python3 <skill-directory>/scripts/check_module.py src/mypackage/ledger_parse.py
```
