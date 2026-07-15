#!/usr/bin/env bash
# Install every primary (top-level) skill in this pack. No arguments needed:
#
#   ./install-all.sh              # install all primary skills for the current user
#   ./install-all.sh --repo PATH  # install all primary skills into a specific repo
#
set -euo pipefail

PACK_ROOT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default to a per-user install; --repo PATH is the only option.
INSTALL_ARGS=(--user)
if [[ $# -ge 1 ]]; then
  case "$1" in
    --user)
      [[ $# -eq 1 ]] || { echo "Usage: $0 [--repo /path/to/repository]" >&2; exit 2; }
      ;;
    --repo)
      [[ $# -eq 2 && -d "$2" ]] || { echo "ERROR: --repo requires an existing repository directory" >&2; exit 2; }
      REPO_ROOT="$(cd -P "$2" && pwd)"
      [[ "$REPO_ROOT" != "/" ]] || { echo "ERROR: refusing to install into the filesystem root" >&2; exit 2; }
      INSTALL_ARGS=(--repo "$REPO_ROOT")
      ;;
    *)
      echo "Usage: $0 [--repo /path/to/repository]" >&2; exit 2
      ;;
  esac
fi

installers=()
while IFS= read -r installer; do
  installers+=("$installer")
done < <(find "$PACK_ROOT" -mindepth 2 -maxdepth 2 -type f -name install.sh -print | LC_ALL=C sort)

[[ ${#installers[@]} -gt 0 ]] || {
  echo "ERROR: no skill directories containing install.sh were found" >&2
  exit 1
}

# Each per-skill installer already refuses unsafe destinations; set -e aborts the
# whole run if any one fails.
for installer in "${installers[@]}"; do
  skill_name="$(basename "$(cd -P "$(dirname "$installer")" && pwd)")"
  echo "Installing $skill_name"
  bash "$installer" "${INSTALL_ARGS[@]}"
done

echo "Installed ${#installers[@]} primary skills. Supplemental skills under extra-skills are opt-in."
