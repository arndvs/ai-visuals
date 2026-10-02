#!/usr/bin/env python3
"""render_loop.py — render a looping MP4 from an HTML visual.

Uses Playwright (headless Chromium) to capture the animation loop and ffmpeg
to encode it. The visual must have a loop mode (like the haskell-to-typescript
visual's Loop control).

Usage:
    python python/render_loop.py <index.html> [--format 4:5] [--out output.mp4]

Requires: pip install playwright && playwright install chromium, plus ffmpeg.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

FORMATS = {
    "4:5": (1080, 1350),
    "1:1": (1080, 1080),
    "16:9": (1920, 1080),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an HTML visual to a looping MP4.")
    parser.add_argument("html", type=Path, help="Path to index.html")
    parser.add_argument("--format", choices=FORMATS.keys(), default="4:5")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--seconds", type=float, default=12.0, help="Loop duration to capture")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"Error: {args.html} not found", file=sys.stderr)
        return 1

    out = args.out or args.html.with_suffix(".mp4")
    width, height = FORMATS[args.format]

    with tempfile.TemporaryDirectory() as tmp:
        frames_dir = Path(tmp) / "frames"
        frames_dir.mkdir()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(args.html.resolve().as_uri())
            page.wait_for_load_state("networkidle")

            # Enable clean view if the visual supports it (removes chrome).
            page.evaluate("document.body.classList.add('clean')")
            page.wait_for_timeout(500)

            fps = 30
            total_frames = int(args.seconds * fps)
            for i in range(total_frames):
                page.screenshot(path=str(frames_dir / f"frame-{i:05d}.png"))
                page.wait_for_timeout(1000 / fps)

            browser.close()

        # Encode frames to MP4 with ffmpeg.
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-i",
                str(frames_dir / "frame-%05d.png"),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(out),
            ],
            check=True,
        )

    print(f"Done: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())