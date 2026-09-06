# Rust recipe

Rust's conventions already implement most of this method, including the one place where this method's default is wrong for the language.

## Layout

```text
src/
    ledger_parse.rs       # the brick, with #[cfg(test)] mod tests at the bottom
    lib.rs
tests/
    rung_02.rs            # seam tests -- integration tests, cumulative
examples/
    ledger_parse.rs       # the demo entry point
tests/golden/
    basic.json
```

## The one deviation: tests live in the file

Elsewhere this method requires a sibling test file. In Rust, unit tests idiomatically live in the same file inside `#[cfg(test)] mod tests`, and that is what the toolchain, the community, and `cargo test` expect. Follow Rust.

The testbench discipline is unchanged: the test module must exercise the brick through its **public** API only, exactly as an outside caller would, even though `#[cfg(test)]` grants it access to private items. Reaching into private state to make a test pass defeats the black box just as thoroughly here as anywhere else.

`tests/` at the crate root is for integration and seam tests, which can only see the public API. That restriction is a feature: the assembly ladder belongs there.

## Header

Module-level doc comment at the top of the file.

```rust
//! PURPOSE    Turn raw ledger text into validated transactions.
//! KIND       CORE
//! CONTRACT   IN:  raw: &str -- may be empty
//!            OUT: Result<Vec<Transaction>, LedgerError>
//!            ERRORS: LedgerError::ShortLine when a non-blank line has < 3 fields
//! GUARANTEES Pure. No I/O, no SystemTime, no rand. Borrows its input, never mutates.
//! TUNING     FIELD_SEPARATOR, MAX_LINE_BYTES
//! DECISIONS  D1: chose Result over panicking on malformed input.
//!                Alternative: assert! and let the caller catch nothing.
//!                Why not: input is user-supplied; malformed data is expected,
//!                not a programmer error. Revisit if: input becomes internal only.
//! LIMITS     Does not handle quoted separators inside fields.
//! TESTBENCH  #[cfg(test)] mod tests below -- run with: cargo test ledger_parse
```

`RAISES` is written `ERRORS` here. Every other field keeps its name.

## Contract expression

The type system carries most of the contract. Use it fully:

- `Result<T, E>` for anything that can fail. Reserve panics for programmer errors, never for bad input.
- A concrete error `enum` with `thiserror`, one variant per documented failure, rather than `Box<dyn Error>` in a public signature.
- Newtypes over primitives at the boundary (`struct Cents(i64)`), so a contract violation becomes a compile error rather than a runtime surprise.
- Borrow (`&str`, `&[T]`) in, own (`String`, `Vec<T>`) out, unless the contract says otherwise. State it in `GUARANTEES`.
- Traits for `SHELL` dependencies a `CORE` brick needs, so tests substitute a fake with no runtime cost.

`#![forbid(unsafe_code)]` in a `CORE` brick unless the crate genuinely needs otherwise.

## Purity

A `CORE` brick must not use `std::fs`, `std::net`, `std::io` (beyond `fmt`), `std::process`, `std::env`, `std::time::SystemTime::now`, or `rand`. Pass the instant and the seed in.

## Testbench

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn contract_parses_two_rows() { /* ... */ }

    #[test]
    fn boundary_empty_input_is_empty_vec() {
        assert_eq!(parse_ledger("").unwrap(), vec![]);
    }

    #[test]
    fn error_short_line() {
        assert!(matches!(parse_ledger("bad"), Err(LedgerError::ShortLine { line: 1 })));
    }

    #[test]
    fn golden_basic() {
        insta::assert_json_snapshot!(parse_ledger(SAMPLE).unwrap());
    }
}
```

Run one testbench: `cargo test ledger_parse`. Run one case: `cargo test ledger_parse::tests::error_short_line -- --exact --nocapture`.

**Goldens** with `insta`. Review changes with `cargo insta review`, which shows the diff and makes accepting a change deliberate rather than automatic.

**Properties** with `proptest`, for `CORE` bricks:

```rust
proptest! {
    #[test]
    fn never_panics_on_arbitrary_input(raw in ".*") {
        let _ = parse_ledger(&raw);   // may Err, must never panic
    }
}
```

**Shell bricks:** contract-tested against a trait fake or `tempfile`; plus one real smoke test behind `#[ignore]` so `cargo test -- --ignored` selects it.

## Demo entry point

`examples/` is Rust's native runnable-demo mechanism. Each file is a separate binary, compiled by `cargo test` so it cannot rot, and runnable on demand:

```rust
// examples/ledger_parse.rs -- demo, not a test. The gate is the tests module.
fn main() {
    let sample = "acct-1|1250|2024-01-01\nacct-2|-300|2024-01-02";
    for t in mycrate::ledger_parse::parse_ledger(sample).unwrap() {
        println!("{t:?}");
    }
}
```

Run with `cargo run --example ledger_parse`.

## Commands to cite as evidence

```bash
cargo test ledger_parse
cargo clippy -- -D warnings
cargo run --example ledger_parse
python3 <skill-directory>/scripts/check_module.py src/ledger_parse.rs
```
