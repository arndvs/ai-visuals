#!/bin/bash
set -euo pipefail

# publish-to-site.sh — copy a finished visual into the arndvs.com checkout.
# Usage: ./tools/publish-to-site.sh <visual-name> <path-to-site-repo>
#
# The site serves it at /visuals/<visual-name>/index.html. Embed it on a case
# study with the DeepDive `embed` field, using ?embed=1 to hide the controls.

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <visual-name> <path-to-site-repo>" >&2
    exit 1
fi

SRC="visuals/$1/index.html"
DEST="$2/public/visuals/$1"

[[ -f "$SRC" ]] || { echo "Error: $SRC not found." >&2; exit 1; }
[[ -d "$2/public" ]] || { echo "Error: $2 does not look like the site repo." >&2; exit 1; }
grep -q "@fonts inlined" "$SRC" || { echo "Error: run tools/inline-fonts.py on $SRC first." >&2; exit 1; }

mkdir -p "$DEST"
cp "$SRC" "$DEST/index.html"
echo "Copied to $DEST/index.html"
