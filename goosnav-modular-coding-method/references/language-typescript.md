# TypeScript recipe

## Layout

```text
src/
    ledgerParse.ts            # the brick
    moneyRound.ts
test/
    ledgerParse.test.ts       # the testbench
    assembly/
        rung02.test.ts
fixtures/
    ledgerParse/goldenBasic.json
```

Vitest is assumed; Jest works identically apart from the runner command and the snapshot API. Follow whichever the project already uses.

## Header

Block comment at the top of the file, before imports.

```ts
/**
 * PURPOSE    Turn raw ledger text into validated transactions.
 * KIND       CORE
 * CONTRACT   IN:  raw: string -- may be empty
 *            OUT: Transaction[] -- source order preserved, may be empty
 *            THROWS: LedgerFormatError when a non-blank line has fewer than 3 fields
 * GUARANTEES Pure. No I/O, no Date.now, no Math.random. Never mutates its input.
 * TUNING     FIELD_SEPARATOR, MAX_LINE_BYTES
 * DECISIONS  D1: chose a discriminated-union result for the caller's error path.
 *                Alternative: throw only. Why not: the CLI needs to report every
 *                bad line, not abort on the first. Revisit if: callers stop
 *                needing partial results.
 * LIMITS     Does not handle quoted separators inside fields.
 * TESTBENCH  test/ledgerParse.test.ts -- run with: npx vitest run test/ledgerParse.test.ts
 */
```

`RAISES` is written `THROWS` here to match the language. Every other field keeps its name.

## Contract expression

Exported `interface` or `type` for every boundary type; never `any`, never an inline anonymous object in a public signature. Discriminated unions for results that can fail without throwing:

```ts
export type ParseResult =
  | { ok: true; transactions: Transaction[] }
  | { ok: false; error: LedgerFormatError };
```

The union forces callers to handle the failure case at compile time, which is contract enforcement the type system does for free.

`zod` belongs in `SHELL` bricks at the process edge -- HTTP bodies, config files, anything untrusted -- where a runtime schema produces both validation and a static type via `z.infer`. Do not run zod inside pure logic that is already statically typed.

Enable `strict` in `tsconfig.json`. Without it the contracts are advisory.

## Purity

A `CORE` brick must not import `node:fs`, `node:path`, `node:http`, `node:crypto`, a database client, or `fetch`, and must not call `Date.now()`, `new Date()` with no argument, `Math.random()`, or read `process.env`. Pass the timestamp, the seed, and the config in.

## Testbench

```ts
import { describe, it, expect } from "vitest";
import { parseLedger, LedgerFormatError } from "../src/ledgerParse.js";

describe("parseLedger", () => {
  it("parses two transactions", () => { /* contract */ });

  it.each(["", "\n", "   \n\n"])("returns [] for blank input %j", (raw) => {
    expect(parseLedger(raw)).toEqual([]);          // boundary
  });

  it("throws on a short line", () => {             // error
    expect(() => parseLedger("a|1|x\nbad")).toThrow(LedgerFormatError);
  });

  it("matches the golden output", () => {          // golden
    expect(parseLedger(SAMPLE)).toMatchSnapshot();
  });
});
```

Run one testbench: `npx vitest run test/ledgerParse.test.ts`. Run one case: `npx vitest run test/ledgerParse.test.ts -t "throws on a short line"`.

**Properties** with `fast-check`, for `CORE` bricks:

```ts
import fc from "fast-check";

it("round-trips any valid transaction list", () => {
  fc.assert(fc.property(arbTransactions(), (xs) =>
    expect(parseLedger(format(xs))).toEqual(xs)));
});
```

**Goldens** with `toMatchSnapshot()` or a checked-in fixture compared verbatim. Review every snapshot change; `-u` regenerates blindly and is how a regression becomes the new expected output.

**Shell bricks:** contract-tested against `msw`, a fake client, or a temp directory; plus one real smoke test.

## Demo entry point

Node has no `__main__`, so guard on the entry module:

```ts
import { fileURLToPath } from "node:url";

// Demo, not a test. The gate is test/ledgerParse.test.ts.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const sample = "acct-1|1250|2024-01-01\nacct-2|-300|2024-01-02";
  console.table(parseLedger(sample));
}
```

Run with `npx tsx src/ledgerParse.ts`. For CommonJS the guard is `if (require.main === module)`.

Note that this import of `node:url` is permitted in a `CORE` brick because it is confined to the demo guard; the checker allows it there and nowhere else. Keep the demo block at the bottom of the file, after the exported logic.

## Commands to cite as evidence

```bash
npx vitest run test/ledgerParse.test.ts
npx tsc --noEmit
npx tsx src/ledgerParse.ts
python3 <skill-directory>/scripts/check_module.py src/ledgerParse.ts
```
