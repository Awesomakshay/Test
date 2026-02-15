#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 daily_brief.py

TODAY="$(date +%F)"
OUTPUT_FILE="briefs/${TODAY}.md"

if [[ -f "$OUTPUT_FILE" ]]; then
  echo ""
  echo "Daily brief generated: $OUTPUT_FILE"
  echo "Open it with:"
  echo "  less $OUTPUT_FILE"
fi
