#!/usr/bin/env python3
"""make_thumbnail.py — capture the first frame of a visual as a PNG thumbnail.

The first frame is the thumbnail: it has to work as a still, because that's
all many people will ever see.

Usage:
    python python/make_thumbnail.py <index.html> [--format 4:5] [--out thumbnail.png]

Requires: pip install playwright && playwright install chromium.
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

FORMATS = {
    "4:5": (1080, 1350),
    "1:1": (1080, 1080),
    "16:9": (1920, 1080),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a visual's first frame as a thumbnail.")
    parser.add_argument("html", type=Path)
    parser.add_argument("--format", choices=FORMATS.keys(), default="4:5")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if not args.html.exists():
        print(f"Error: {args.html} not found", file=sys.stderr)
        return 1

    out = args.out or args.html.with_name("thumbnail.png")
    width, height = FORMATS[args.format]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(args.html.resolve().as_uri())
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(800)  # let the first frame settle
        page.screenshot(path=str(out))
        browser.close()

    print(f"Done: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())