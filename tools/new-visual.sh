#!/bin/bash
set -euo pipefail

# new-visual.sh — scaffold a new visual folder from the template.
# Usage: ./tools/new-visual.sh <visual-name>

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <visual-name>" >&2
    exit 1
fi

NAME="$1"
DIR="visuals/$NAME"

if [[ -e "$DIR" ]]; then
    echo "Error: $DIR already exists." >&2
    exit 1
fi

mkdir -p "$DIR"
cp templates/index.html "$DIR/index.html"
cp templates/visual-README.md "$DIR/README.md"

echo "Created $DIR/"
echo "Next: edit $DIR/index.html and $DIR/README.md, then ship."