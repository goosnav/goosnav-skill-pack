#!/usr/bin/env bash
# Double-click this file in Finder (macOS) to install every skill in the pack
# for the current user. It just runs install-all.sh from its own folder.
set -euo pipefail

cd "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
./install-all.sh

echo
echo "Done. Press Return to close this window."
read -r _
