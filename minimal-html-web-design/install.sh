#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="minimal-html-web-design"
SOURCE_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() { echo "Usage: $0 [--user | --repo /path/to/repository]" >&2; exit 2; }

copy_skill() {
  local root="$1" destination staging
  destination="$root/$SKILL_NAME"
  [[ "$destination" != "$SOURCE_DIR" && "$destination" != "$SOURCE_DIR/"* ]] || {
    echo "ERROR: refusing a destination inside the source skill" >&2; exit 2;
  }
  mkdir -p "$root"
  staging="$(mktemp -d "$root/.${SKILL_NAME}.tmp.XXXXXX")"
  trap 'rm -rf "${staging:-}"' EXIT
  cp -R "$SOURCE_DIR/." "$staging/"
  rm -rf "$destination"
  mv "$staging" "$destination"
  trap - EXIT
  echo "Installed: $destination"
}

remove_legacy() {
  local destination="$1/$SKILL_NAME"
  [[ -e "$destination" ]] || return 0
  [[ "$destination" != "$SOURCE_DIR" ]] || { echo "Retained active source: $destination"; return; }
  rm -rf "$destination"
  echo "Removed same-name legacy copy: $destination"
}

case "${1:---user}" in
  --user)
    [[ $# -le 1 && -n "${HOME:-}" && "$HOME" != "/" && -d "$HOME" ]] || usage
    copy_skill "$HOME/.agents/skills"
    remove_legacy "$HOME/.codex/skills"
    remove_legacy "$HOME/.claude/skills"
    ;;
  --repo)
    [[ $# -eq 2 && -d "$2" ]] || usage
    root="$(cd -P "$2" && pwd)"
    [[ "$root" != "/" ]] || { echo "ERROR: refusing filesystem root" >&2; exit 2; }
    copy_skill "$root/.agents/skills"
    remove_legacy "$root/.codex/skills"
    remove_legacy "$root/.claude/skills"
    ;;
  *) usage ;;
esac
