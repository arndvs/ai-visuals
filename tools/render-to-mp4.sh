#!/bin/bash
set -euo pipefail

# render-to-mp4.sh — render an HTML visual to MP4 via HyperFrames.
# Usage: ./tools/render-to-mp4.sh <path-to-index.html> [output.mp4]

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <path-to-index.html> [output.mp4]" >&2
    exit 1
fi

HTML="$1"
OUT="${2:-${HTML%.html}.mp4}"

if ! command -v hyperframes &>/dev/null; then
    echo "HyperFrames CLI not found. Install with: npx skills add heygen-com/hyperframes" >&2
    exit 1
fi

echo "Rendering $HTML → $OUT"
hyperframes render "$HTML" --output "$OUT"
echo "Done: $OUT"