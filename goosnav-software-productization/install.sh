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
    echo "Already canonical: $destination"
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

remove_legacy() {
  local destination="$1/$SKILL_NAME"
  [[ -e "$destination" ]] || return 0
  if [[ "$(cd "$(dirname "$destination")" && pwd)/$(basename "$destination")" == "$SOURCE_DIR" ]]; then
    echo "Legacy source copy retained while installer is running: $destination"
    return
  fi
  rm -rf "$destination"
  echo "Removed duplicate: $destination"
}

case "$MODE" in
  --user)
    copy_skill "$HOME/.agents/skills"
    remove_legacy "$HOME/.codex/skills"
    remove_legacy "$HOME/.claude/skills"
    echo "Canonical Agent Skill: $HOME/.agents/skills/$SKILL_NAME"
    ;;
  --repo)
    if [[ -z "$REPO_PATH" ]]; then
      echo "Usage: $0 --repo /path/to/repository" >&2
      exit 2
    fi
    REPO_PATH="$(cd "$REPO_PATH" && pwd)"
    copy_skill "$REPO_PATH/.agents/skills"
    remove_legacy "$REPO_PATH/.codex/skills"
    remove_legacy "$REPO_PATH/.claude/skills"
    echo "Canonical repository skill: $REPO_PATH/.agents/skills/$SKILL_NAME"
    ;;
  *)
    echo "Usage: $0 --user | --repo /path/to/repository" >&2
    exit 2
    ;;
esac
