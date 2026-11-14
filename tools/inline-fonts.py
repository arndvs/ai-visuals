#!/usr/bin/env python3
"""Inline the site fonts into a visual so the HTML file has no dependencies.

Usage: python3 tools/inline-fonts.py visuals/<name>/index.html

Replaces the block between /*@fonts and /*@end-fonts*/ with base64 @font-face
rules built from python/site_images/fonts/. Safe to run twice.
"""
import base64
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FONTS = REPO / "python" / "site_images" / "fonts"
FACES = [("Outfit", 800, "Outfit-ExtraBold.woff"), ("DM Sans", 500, "DMSans-500.woff"), ("DM Sans", 700, "DMSans-700.woff")]


def face(family: str, weight: int, filename: str) -> str:
    data = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (
        f'@font-face {{ font-family: "{family}"; font-weight: {weight}; '
        f'src: url("data:font/woff;base64,{data}") format("woff"); font-display: swap; }}'
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    path = pathlib.Path(sys.argv[1])
    html = path.read_text()
    try:
        start = html.index("/*@fonts")
        end = html.index("/*@end-fonts*/") + len("/*@end-fonts*/")
    except ValueError:
        print(f"{path}: no /*@fonts ... /*@end-fonts*/ block found")
        return 1
    block = "/*@fonts inlined */\n" + "\n".join(face(*f) for f in FACES) + "\n/*@end-fonts*/"
    path.write_text(html[:start] + block + html[end:])
    print(f"Inlined {len(FACES)} fonts into {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
