#!/usr/bin/env python3
"""crop_screenshot.py — crop a browser screenshot to the 2:1 shape used on arndvs.com.

Keeps the full height and the left 2x-height pixels, which drops the scrollbar and any
cursor parked at the right edge. Saves a JPEG.

Usage:
    python python/site_images/crop_screenshot.py <screenshot> <out.jpg>

Requires: pip install pillow.
"""

import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description="Crop a screenshot to 2:1.")
    parser.add_argument("src", type=Path)
    parser.add_argument("dst", type=Path)
    args = parser.parse_args()

    im = Image.open(args.src).convert("RGB")
    w, h = im.size
    if w < h * 2:
        parser.error(f"{args.src} is {w}x{h}; it needs to be at least twice as wide as it is tall")
    im = im.crop((0, 0, h * 2, h))
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(args.dst, "JPEG", quality=90, optimize=True)
    print(f"wrote {args.dst} {im.size[0]}x{im.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
