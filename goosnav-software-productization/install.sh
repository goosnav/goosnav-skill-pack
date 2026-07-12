#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="goosnav-software-productization"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---user}"
REPO_PATH="${2:-}"

copy_skill() {
  local destination_root="$1"
  local destination="$destination_root/$SKILL_NAME"
  mkdir -p "$destination_root"
  if [[ "$(cd "$(dirname "$destination")" && pwd)/$(basename "$destination")" == "$SOURCE_DIR" ]]; then
    echo "Already installed: $destination"
    return
  fi
  local staging
  staging="$(mktemp -d)"
  cp -R "$SOURCE_DIR" "$staging/$SKILL_NAME"
  rm -rf "$destination"
  mv "$staging/$SKILL_NAME" "$destination"
  rmdir "$staging"
  echo "Installed: $destination"
}

case "$MODE" in
  --user)
    copy_skill "$HOME/.claude/skills"
    copy_skill "$HOME/.agents/skills"
    echo "Claude Code: /$SKILL_NAME"
    echo "Codex:       \$$SKILL_NAME"
    ;;
  --repo)
    if [[ -z "$REPO_PATH" ]]; then
      echo "Usage: $0 --repo /path/to/repository" >&2
      exit 2
    fi
    REPO_PATH="$(cd "$REPO_PATH" && pwd)"
    copy_skill "$REPO_PATH/.claude/skills"
    copy_skill "$REPO_PATH/.agents/skills"
    echo "Installed repository-scoped copies in: $REPO_PATH"
    ;;
  *)
    echo "Usage: $0 --user | --repo /path/to/repository" >&2
    exit 2
    ;;
esac
