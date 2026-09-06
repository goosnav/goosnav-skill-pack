#!/usr/bin/env bash
# Double-click this file in Finder (macOS) to install the Aesthetic Web Design skill
# for the current user. It just runs install.sh from its own folder.
#
# Destination is ~/.agents/skills/aesthetic-web-design, which both
# Claude Code and Codex read. Only same-name legacy copies under
# ~/.claude/skills and ~/.codex/skills are removed; nothing else is touched.
#
# Deliberately no `set -e`: a double-clicked window closes the instant the
# script exits, so a failure has to be caught and reported before the pause
# rather than aborting straight past it.

cd "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || {
  echo "ERROR: could not enter the skill folder."
  echo "Press Return to close this window."
  read -r _
  exit 1
}

./install.sh --user
status=$?

echo
if [[ $status -eq 0 ]]; then
  echo "Restart Claude Code or Codex to pick up the skill."
else
  echo "Install failed with exit status $status. The message above says why."
fi
echo "Press Return to close this window."
read -r _
exit "$status"
