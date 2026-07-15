#!/usr/bin/env bash
# Collect reproducible code-health evidence without installing tools.
# Some analyzers write caches; tests execute repository code and are opt-in.

set -uo pipefail

SCRIPT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: codebase-audit.sh [--source DIR] [--output DIR] [--run-tests] [--allow-network]

The default output is a fresh temporary directory. Exit status is:
  0  all executed checks passed (skipped checks may still remain)
  1  findings or test/check failures require review
  2  a tool or audit command errored

This collector is triage evidence, not a release verdict. It never installs tools.
Review repository trust first: tools and tests may execute code or create caches.
EOF
}

SOURCE_DIR="."
OUTPUT_DIR=""
RUN_TESTS=0
ALLOW_NETWORK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; SOURCE_DIR="$2"; shift 2 ;;
    --output) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; OUTPUT_DIR="$2"; shift 2 ;;
    --run-tests) RUN_TESTS=1; shift ;;
    --allow-network) ALLOW_NETWORK=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      # Preserve the draft script's single positional source-directory interface.
      if [[ "$SOURCE_DIR" == "." && -d "$1" ]]; then SOURCE_DIR="$1"; shift
      else echo "ERROR: unknown argument: $1" >&2; usage >&2; exit 2
      fi
      ;;
  esac
done

[[ -d "$SOURCE_DIR" ]] || { echo "ERROR: source directory does not exist: $SOURCE_DIR" >&2; exit 2; }
SOURCE_DIR="$(cd -P "$SOURCE_DIR" && pwd)"
RUN_ID="$(date -u '+%Y%m%dT%H%M%SZ')-$$"
if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/goosnav-code-audit.${RUN_ID}.XXXXXX")" || exit 2
fi
mkdir -p "$OUTPUT_DIR" || exit 2
OUTPUT_DIR="$(cd -P "$OUTPUT_DIR" && pwd)"

STATUS_FILE="$OUTPUT_DIR/status.tsv"
TOOLS_FILE="$OUTPUT_DIR/tools.tsv"
printf 'id\tstatus\texit_code\tduration_seconds\tlog\tcommand\n' > "$STATUS_FILE"
printf 'tool\tversion\n' > "$TOOLS_FILE"

has_command() { command -v "$1" >/dev/null 2>&1; }

sanitize() { printf '%s' "$1" | tr '\t\n' '  '; }

record_tool() {
  local tool="$1" version
  if has_command "$tool"; then
    version="$($tool --version 2>&1 | head -1 || true)"
    printf '%s\t%s\n' "$(sanitize "$tool")" "$(sanitize "$version")" >> "$TOOLS_FILE"
  fi
}

skip_check() {
  local id="$1" title="$2" reason="$3" log
  log="$OUTPUT_DIR/$id.txt"
  printf '%s\nReason: %s\n' "$title" "$reason" > "$log"
  printf '%s\tSKIPPED\t\t0\t%s\t%s\n' "$id" "$(sanitize "$log")" "$(sanitize "$reason")" >> "$STATUS_FILE"
  printf '[SKIPPED] %s — %s\n' "$title" "$reason"
}

run_check() {
  local id="$1" title="$2" mode="$3"
  shift 3
  local log="$OUTPUT_DIR/$id.txt" command start end duration rc status
  command="$(printf '%q ' "$@")"
  start="$(date +%s)"
  printf '%s\nCommand: %s\n\n' "$title" "$command" > "$log"
  set +e
  "$@" >> "$log" 2>&1
  rc=$?
  set -e
  end="$(date +%s)"
  duration=$((end - start))
  if [[ $rc -eq 0 ]]; then
    status="PASS"
  elif [[ "$mode" == "analyzer" && $rc -eq 1 ]]; then
    status="FINDINGS"
  elif [[ "$mode" == "test" && $rc -eq 1 ]]; then
    status="FAIL"
  elif [[ "$mode" == "check" ]]; then
    status="FAIL"
  else
    status="ERROR"
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$id" "$status" "$rc" "$duration" "$(sanitize "$log")" "$(sanitize "$command")" >> "$STATUS_FILE"
  printf '[%s] %s (exit %s, %ss)\n' "$status" "$title" "$rc" "$duration"
}

largest_source_files() {
  find . \
    \( -path './.git' -o -path './.code-audit' -o -path './.venv' -o -path './venv' \
       -o -path './node_modules' -o -path './build' -o -path './dist' -o -path './target' \) -prune -o \
    -type f \( -name '*.py' -o -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \
      -o -name '*.go' -o -name '*.rs' -o -name '*.java' -o -name '*.rb' -o -name '*.sh' \) \
    -exec wc -l {} + | sort -nr | sed -n '1,50p'
}

debt_markers() {
  local output rc
  output="$(rg --line-number --hidden \
    --glob '!.git/**' --glob '!.code-audit/**' --glob '!.venv/**' --glob '!venv/**' \
    --glob '!node_modules/**' --glob '!build/**' --glob '!dist/**' --glob '!target/**' \
    'TODO|FIXME|HACK|XXX|NotImplemented|NotImplementedError' . 2>&1)"
  rc=$?
  printf '%s\n' "$output"
  [[ $rc -eq 1 ]] && return 0
  [[ $rc -eq 0 ]] && return 1
  return "$rc"
}

radon_complexity() {
  local output rc
  output="$(radon cc . --show-complexity --average --min C \
    --exclude '*/.venv/*,*/venv/*,*/node_modules/*,*/build/*,*/dist/*' 2>&1)"
  rc=$?
  printf '%s\n' "$output"
  [[ $rc -ne 0 ]] && return "$rc"
  printf '%s\n' "$output" | grep -Eq ' - [C-F] \([0-9]+\)' && return 1
  return 0
}

radon_maintainability() {
  local output rc
  output="$(radon mi . --show \
    --exclude '*/.venv/*,*/venv/*,*/node_modules/*,*/build/*,*/dist/*' 2>&1)"
  rc=$?
  printf '%s\n' "$output"
  [[ $rc -ne 0 ]] && return "$rc"
  printf '%s\n' "$output" | grep -Eq ' - C( |$)' && return 1
  return 0
}

vulture_findings() {
  local output rc
  output="$(vulture . --min-confidence 80 --exclude '.venv,venv,node_modules,build,dist' 2>&1)"
  rc=$?
  printf '%s\n' "$output"
  [[ $rc -ne 0 ]] && return "$rc"
  [[ -n "$output" ]] && return 1
  return 0
}

shell_files_check() {
  find . -type f -name '*.sh' \
    -not -path './.git/*' -not -path './.code-audit/*' -not -path './node_modules/*' \
    -print0 | xargs -0 shellcheck
}

write_context() {
  {
    echo "run_id=$RUN_ID"
    echo "generated_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo "source=$SOURCE_DIR"
    echo "output=$OUTPUT_DIR"
    echo "run_tests=$RUN_TESTS"
    echo "allow_network=$ALLOW_NETWORK"
    echo "uname=$(uname -a)"
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      echo "git_commit=$(git rev-parse HEAD 2>/dev/null || true)"
      echo "git_branch=$(git branch --show-current 2>/dev/null || true)"
      echo "git_status_begin"
      git status --short
      echo "git_status_end"
    else
      echo "git_repository=false"
    fi
  } > "$OUTPUT_DIR/context.txt"
}

cd "$SOURCE_DIR" || exit 2
write_context

for tool in git rg tokei shellcheck ruff radon vulture mypy bandit pytest pip-audit \
  node npm eslint tsc gitleaks semgrep trivy go govulncheck cargo cargo-audit; do
  record_tool "$tool"
done

echo "Codebase health evidence run: $RUN_ID"
echo "Repository: $SOURCE_DIR"
echo "Reports: $OUTPUT_DIR"

run_check "01-largest-source-files" "Largest source files" check largest_source_files
if has_command rg; then run_check "02-debt-markers" "Debt and incomplete-code markers" analyzer debt_markers
else skip_check "02-debt-markers" "Debt and incomplete-code markers" "rg is unavailable"; fi
if has_command tokei; then run_check "03-language-metrics" "Language and line-count metrics" check tokei .
else skip_check "03-language-metrics" "Language and line-count metrics" "tokei is unavailable"; fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  run_check "04-git-diff-check" "Git whitespace and conflict-marker check" check git diff --check
else skip_check "04-git-diff-check" "Git whitespace and conflict-marker check" "not a Git repository"; fi

if find . -type f -name '*.sh' -not -path './.git/*' -not -path './.code-audit/*' -print -quit | grep -q .; then
  if has_command shellcheck; then run_check "10-shellcheck" "Shell static analysis" analyzer shell_files_check
  else skip_check "10-shellcheck" "Shell static analysis" "shellcheck is unavailable"; fi
fi

if find . -type f -name '*.py' -not -path './.git/*' -not -path './.code-audit/*' -print -quit | grep -q .; then
  if has_command ruff; then run_check "20-ruff" "Python lint (Ruff)" analyzer ruff check . --no-cache --output-format=concise
  else skip_check "20-ruff" "Python lint (Ruff)" "ruff is unavailable"; fi
  if has_command radon; then
    run_check "21-radon-cc-c-f" "Python cyclomatic complexity C through F" analyzer radon_complexity
    run_check "22-radon-mi" "Python maintainability index C results" analyzer radon_maintainability
  else
    skip_check "21-radon-cc-c-f" "Python cyclomatic complexity C through F" "radon is unavailable"
    skip_check "22-radon-mi" "Python maintainability index" "radon is unavailable"
  fi
  if has_command vulture; then run_check "23-vulture" "Possible Python dead code" analyzer vulture_findings
  else skip_check "23-vulture" "Possible Python dead code" "vulture is unavailable"; fi
  if has_command mypy; then run_check "24-mypy" "Python type checking using repository config" analyzer mypy . --show-error-codes --cache-dir "$OUTPUT_DIR/mypy-cache"
  else skip_check "24-mypy" "Python type checking" "mypy is unavailable"; fi
  if has_command bandit; then run_check "25-bandit" "Python security static analysis" analyzer bandit -r . -x './.venv,./venv,./node_modules,./build,./dist,./.code-audit' -f screen
  else skip_check "25-bandit" "Python security static analysis" "bandit is unavailable"; fi
  if [[ $RUN_TESTS -eq 1 ]]; then
    if has_command pytest; then run_check "26-pytest" "Python test suite (executes repository code)" test env PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider
    else skip_check "26-pytest" "Python test suite" "pytest is unavailable"; fi
  else skip_check "26-pytest" "Python test suite" "requires explicit --run-tests after repository trust review"; fi
  if [[ $ALLOW_NETWORK -eq 1 && -f requirements.txt ]] && has_command pip-audit; then
    run_check "27-pip-audit" "Python dependency advisory scan from requirements.txt" analyzer pip-audit -r requirements.txt
  elif [[ -f requirements.txt ]]; then
    skip_check "27-pip-audit" "Python dependency advisory scan" "requires pip-audit and explicit --allow-network"
  fi
fi

if [[ -f package.json ]]; then
  if [[ -x node_modules/.bin/eslint ]]; then run_check "30-eslint" "JavaScript/TypeScript lint" analyzer node_modules/.bin/eslint .
  else skip_check "30-eslint" "JavaScript/TypeScript lint" "project-local eslint is unavailable; use the repository-native command"; fi
  if [[ -x node_modules/.bin/tsc ]]; then run_check "31-typescript" "TypeScript type checking" analyzer node_modules/.bin/tsc --noEmit
  else skip_check "31-typescript" "TypeScript type checking" "project-local tsc is unavailable or not applicable"; fi
  if [[ $RUN_TESTS -eq 1 ]] && has_command npm; then run_check "32-npm-test" "Node test script (executes repository code)" test npm test
  else skip_check "32-npm-test" "Node test script" "requires npm and explicit --run-tests"; fi
  if [[ $ALLOW_NETWORK -eq 1 && -f package-lock.json ]] && has_command npm; then
    run_check "33-npm-audit" "Node dependency advisory scan" analyzer npm audit --audit-level=moderate
  elif [[ -f package-lock.json ]]; then
    skip_check "33-npm-audit" "Node dependency advisory scan" "requires npm and explicit --allow-network"
  fi
fi

if [[ -f go.mod ]]; then
  if has_command go; then
    run_check "40-go-vet" "Go static analysis" check go vet ./...
    if [[ $RUN_TESTS -eq 1 ]]; then run_check "41-go-test" "Go test suite" test go test ./...
    else skip_check "41-go-test" "Go test suite" "requires explicit --run-tests"; fi
  else skip_check "40-go-vet" "Go static analysis" "go is unavailable"; fi
  if has_command govulncheck; then run_check "42-govulncheck" "Go vulnerability scan" analyzer govulncheck ./...
  else skip_check "42-govulncheck" "Go vulnerability scan" "govulncheck is unavailable"; fi
fi

if [[ -f Cargo.toml ]]; then
  if has_command cargo; then
    run_check "50-cargo-check" "Rust compile check" check cargo check --all-targets
    if [[ $RUN_TESTS -eq 1 ]]; then run_check "51-cargo-test" "Rust test suite" test cargo test
    else skip_check "51-cargo-test" "Rust test suite" "requires explicit --run-tests"; fi
  else skip_check "50-cargo-check" "Rust compile check" "cargo is unavailable"; fi
  if has_command cargo-audit; then run_check "52-cargo-audit" "Rust dependency advisory scan" analyzer cargo audit
  else skip_check "52-cargo-audit" "Rust dependency advisory scan" "cargo-audit is unavailable"; fi
fi

if has_command gitleaks; then
  run_check "60-gitleaks" "Working-tree secret scan" analyzer gitleaks detect --source . --no-git --redact
else skip_check "60-gitleaks" "Working-tree secret scan" "gitleaks is unavailable"; fi
if [[ $ALLOW_NETWORK -eq 1 ]] && has_command semgrep; then
  run_check "61-semgrep" "Cross-language Semgrep auto scan" analyzer semgrep scan --error --config auto .
else skip_check "61-semgrep" "Cross-language Semgrep auto scan" "requires semgrep and explicit --allow-network"; fi
if has_command trivy; then run_check "62-trivy" "Filesystem vulnerability and misconfiguration scan" analyzer trivy fs --exit-code 1 --scanners vuln,misconfig,secret .
else skip_check "62-trivy" "Filesystem vulnerability and misconfiguration scan" "trivy is unavailable"; fi

if command -v python3 >/dev/null 2>&1; then
  python3 "$SCRIPT_DIR/summarize-audit.py" "$OUTPUT_DIR" || true
fi

if awk -F '\t' 'NR > 1 && $2 == "ERROR" { found=1 } END { exit !found }' "$STATUS_FILE"; then
  echo "AUDIT RESULT: ERROR — one or more audit commands could not run correctly."
  exit 2
fi
if awk -F '\t' 'NR > 1 && ($2 == "FINDINGS" || $2 == "FAIL") { found=1 } END { exit !found }' "$STATUS_FILE"; then
  echo "AUDIT RESULT: REVIEW REQUIRED — findings or failed checks are present."
  exit 1
fi
echo "AUDIT RESULT: EXECUTED CHECKS PASSED — inspect SKIPPED coverage before drawing conclusions."
exit 0
