#!/usr/bin/env python3
"""Inline the site fonts into a visual so the HTML file has no dependencies.

Usage: python3 tools/inline-fonts.py visuals/<name>/index.html

Replaces the block between /*@fonts and /*@end-fonts*/ with base64 @font-face
rules built from python/site_images/fonts/. Safe to run twice.

The fonts come from the block itself: each @font-face that points at a file in
python/site_images/fonts/ is inlined with its family and weight. The inlined
block records those faces in its opening comment, so a second run rebuilds the
same set. A block with neither falls back to the original site faces (Outfit
and DM Sans), so older visuals behave as before.
"""
import base64
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FONTS = REPO / "python" / "site_images" / "fonts"
FACES = [("Outfit", 800, "Outfit-ExtraBold.woff"), ("DM Sans", 500, "DMSans-500.woff"), ("DM Sans", 700, "DMSans-700.woff")]

DECLARED = re.compile(
    r'font-family:\s*"(?P<family>[^"]+)";\s*font-weight:\s*(?P<weight>\d+);\s*'
    r'src:\s*url\("[^"]*?/fonts/(?P<file>[^"/]+\.woff2?)"\)'
)
RECORDED = re.compile(r"/\*@fonts inlined: (?P<faces>[^*]+)\*/")


def face(family: str, weight: int, filename: str) -> str:
    data = base64.b64encode((FONTS / filename).read_bytes()).decode()
    kind = "woff2" if filename.endswith(".woff2") else "woff"
    return (
        f'@font-face {{ font-family: "{family}"; font-weight: {weight}; '
        f'src: url("data:font/{kind};base64,{data}") format("{kind}"); font-display: swap; }}'
    )


def faces_in(block: str) -> list[tuple[str, int, str]]:
    declared = [(m["family"], int(m["weight"]), m["file"]) for m in DECLARED.finditer(block)]
    if declared:
        return declared
    recorded = RECORDED.search(block)
    if recorded:
        entries = [entry.strip().split("|") for entry in recorded["faces"].split(";") if entry.strip()]
        return [(family, int(weight), file) for family, weight, file in entries]
    return FACES


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
    faces = faces_in(html[start:end])
    record = "; ".join(f"{family}|{weight}|{file}" for family, weight, file in faces)
    block = f"/*@fonts inlined: {record} */\n" + "\n".join(face(*f) for f in faces) + "\n/*@end-fonts*/"
    path.write_text(html[:start] + block + html[end:])
    print(f"Inlined {len(faces)} fonts into {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
