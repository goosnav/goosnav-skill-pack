# Go recipe

Go's own conventions already implement most of this method. Use them rather than importing foreign idioms.

## Layout

```text
internal/ledger/
    parse.go              # the brick
    parse_test.go         # the testbench, same package
    testdata/
        golden_basic.json # `testdata` is ignored by the toolchain by convention
cmd/parsedemo/
    main.go               # the demo entry point
internal/assembly/
    rung02_test.go        # seam tests, cumulative
```

One brick is one file with one exported function. `parse_test.go` sits beside it in the same package so it can be a true testbench while still having access to the package for table setup; assert only through the exported API.

## Header

Doc comment above the package or the exported function.

```go
// PURPOSE    Turn raw ledger text into validated transactions.
// KIND       CORE
// CONTRACT   IN:  raw string -- UTF-8, may be empty
//            OUT: []Transaction -- source order preserved, may be empty
//            ERRORS: ErrShortLine when a non-blank line has fewer than 3 fields
// GUARANTEES Pure. No I/O, no time.Now, no rand. Never mutates its input.
// TUNING     fieldSeparator, maxLineBytes
// DECISIONS  D1: chose a sentinel error over a typed struct error.
//                Alternative: a LedgerError type with a line field.
//                Why not: callers only branch on kind, not on detail.
//                Revisit if: a caller needs the line number programmatically.
// LIMITS     Does not handle quoted separators inside fields.
// TESTBENCH  parse_test.go -- run with: go test ./internal/ledger -run TestParse -v
func ParseLedger(raw string) ([]Transaction, error) {
```

`RAISES` is written `ERRORS` here, matching Go's model. Every other field keeps its name.

## Contract expression

Named struct types at every boundary; no `map[string]interface{}` in an exported signature. Errors are values returned explicitly, declared as sentinels and matched with `errors.Is`:

```go
var ErrShortLine = errors.New("ledger: line has fewer than 3 fields")
```

Small interfaces defined at the **consumer**, not the producer -- that is the Go way to express a `SHELL` dependency a `CORE` brick can be tested against. One or two methods; if an interface has five, it is not a seam.

## Purity

A `CORE` brick must not import `os`, `io`, `net`, `net/http`, `database/sql`, `math/rand`, `time` (for `Now`), or `os/exec`. Pass the timestamp and the seed in. `time.Time` as a value type is fine; `time.Now()` as a call is not.

## Testbench

Table-driven, which is the Go standard and maps directly onto the case taxonomy:

```go
func TestParseLedger(t *testing.T) {
	tests := []struct {
		name    string
		raw     string
		want    []Transaction
		wantErr error
	}{
		{name: "contract/two rows", raw: twoRows, want: twoParsed},
		{name: "boundary/empty", raw: "", want: nil},
		{name: "boundary/blank lines only", raw: "\n\n", want: nil},
		{name: "error/short line", raw: "bad", wantErr: ErrShortLine},
	}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got, err := ParseLedger(tc.raw)
			if !errors.Is(err, tc.wantErr) {
				t.Fatalf("err = %v, want %v", err, tc.wantErr)
			}
			if diff := cmp.Diff(tc.want, got); diff != "" {
				t.Errorf("mismatch (-want +got):\n%s", diff)
			}
		})
	}
}
```

Run one testbench: `go test ./internal/ledger -v`. Run one case: `go test ./internal/ledger -run 'TestParseLedger/error/short_line' -v`.

**Goldens** use the idiomatic `-update` flag with `testdata/`:

```go
var update = flag.Bool("update", false, "rewrite golden files")
// compare against testdata/golden_basic.json; rewrite it only when -update is passed
```

Regenerate with `go test ./internal/ledger -update` as a deliberate act, and review the `testdata` diff.

**Examples** are Go's native runnable-documentation mechanism and are worth having in addition to the table: an `Example` function is compiled, executed, and its `// Output:` comment verified by `go test`, so it can never rot.

```go
func ExampleParseLedger() {
	txs, _ := ParseLedger("acct-1|1250|2024-01-01")
	fmt.Println(txs[0].Identifier)
	// Output: acct-1
}
```

**Properties** with `testing/quick` for simple invariants, or `pgregory.net/rapid` for real generators.

**Shell bricks:** contract-tested against a `httptest.Server`, `t.TempDir()`, or a fake satisfying the consumer interface; plus one real smoke test behind `testing.Short()`.

## Demo entry point

Go has no in-file main guard. The demo is a tiny `cmd/` program, which is the idiomatic equivalent and has the advantage of proving the brick is usable from outside its package:

```go
// cmd/parsedemo/main.go -- demo, not a test. The gate is internal/ledger/parse_test.go.
func main() {
	for _, t := range must(ledger.ParseLedger(sample)) {
		fmt.Printf("%+v\n", t)
	}
}
```

Run with `go run ./cmd/parsedemo`.

## Commands to cite as evidence

```bash
go test ./internal/ledger -v
go vet ./internal/ledger
go run ./cmd/parsedemo
python3 <skill-directory>/scripts/check_module.py internal/ledger/parse.go
```
