#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p briefs
LOG_FILE="briefs/last_run.log"

python3 daily_brief.py --preview | tee "$LOG_FILE"

TODAY="$(date +%F)"
OUTPUT_FILE="briefs/${TODAY}.md"

echo ""
echo "Daily brief generated: $OUTPUT_FILE"
echo "Run log saved at     : $LOG_FILE"

echo ""
echo "Open the brief with:"
echo "  less $OUTPUT_FILE"

echo ""
if [[ -t 1 ]]; then
  read -r -p "Press Enter to close..." _
fi
