#!/bin/bash
set -euo pipefail

# serve.sh — serve the repo locally for previewing visuals.
# Usage: ./tools/serve.sh [port]

PORT="${1:-8000}"

if command -v python3 &>/dev/null; then
    exec python3 -m http.server "$PORT"
elif command -v python &>/dev/null; then
    exec python -m http.server "$PORT"
else
    echo "No python found. Install python3 or use another static server." >&2
    exit 1
fi