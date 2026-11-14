#!/usr/bin/env python3
"""generate_placeholders.py — wireframe placeholders for screens that can't be captured yet.

A placeholder stands in for a real screenshot of a gated or internal screen. It is drawn
in the palette of the product it stands in for (here MCRDSE), not the arndvs.com palette,
so it sits naturally next to real screenshots of the same product. Every placeholder
carries a "Screenshot coming soon" tag and is replaced as soon as a real capture exists.

Usage:
    python python/site_images/generate_placeholders.py [--out DIR] [--site PATH_TO_ARNDVS_REPO]

Requires: pip install pillow.
"""

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from style import DEFAULT_OUT, display, save_jpeg, text

W, H = 1518, 759  # 2:1, the same shape as the cropped screenshots

# MCRDSE palette, sampled from mcrdse.com
CREAM = (243, 234, 221)
PLUM = (31, 10, 60)
PURPLE = (109, 31, 209)
LILAC = (221, 204, 250)
RULE = (214, 200, 186)
BLOCK = (229, 217, 203)
BLOCK_ALT = (236, 226, 240)
MUTED = (112, 96, 128)
PAPER = (250, 246, 240)
LIME = (224, 240, 170)


def base(title, subtitle):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    d.text((64, 24), "mcrdse", font=display(30), fill=PLUM)
    for x in (1210, 1290, 1370):
        d.rounded_rectangle((x, 34, x + 58, 46), 6, fill=BLOCK)
    d.line((0, 82, W, 82), fill=RULE, width=1)
    d.text((96, 118), subtitle.upper(), font=text(15, 700), fill=PURPLE)
    d.text((96, 142), title, font=display(46), fill=PLUM)
    tag, tf = "Screenshot coming soon", text(16, 700)
    tw = d.textlength(tag, font=tf)
    right = W - 96
    d.rounded_rectangle((right - tw - 36, 150, right, 190), 20, fill=PLUM)
    d.text((right - tw - 18, 159), tag, font=tf, fill=PAPER)
    return im, d


def bar(d, x, y, w, h=12, fill=BLOCK):
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=fill)


def card(d, box, fill=PAPER):
    d.rounded_rectangle(box, 18, fill=fill, outline=RULE, width=1)


def small_label(d, x, y, s):
    d.text((x, y), s, font=text(14, 700), fill=MUTED)


def super_market():
    im, d = base("Super Market", "Member storefront · mcrdse.shop")
    x0, y0, cw, ch, gap = 96, 236, 312, 440, 26
    for i in range(4):
        x = x0 + i * (cw + gap)
        card(d, (x, y0, x + cw, y0 + ch))
        d.rounded_rectangle(
            (x + 20, y0 + 20, x + cw - 20, y0 + 250), 12, fill=BLOCK_ALT if i % 2 else BLOCK
        )
        bar(d, x + 20, y0 + 276, 190, 16, PLUM)
        bar(d, x + 20, y0 + 306, 250)
        bar(d, x + 20, y0 + 328, 170)
        bar(d, x + 20, y0 + 376, 70, 22, PLUM)
        d.rounded_rectangle((x + cw - 130, y0 + 368, x + cw - 20, y0 + 408), 20, fill=PURPLE)
    return im


def points_ledger():
    im, d = base("Points & Tiers", "Loyalty account · points ledger")
    card(d, (96, 236, 560, 676))
    small_label(d, 124, 262, "TIER")
    bar(d, 124, 292, 220, 26, PLUM)
    d.rounded_rectangle((124, 356, 532, 376), 10, fill=BLOCK)
    d.rounded_rectangle((124, 356, 372, 376), 10, fill=PURPLE)
    for i, x in enumerate((124, 328, 532)):
        d.ellipse((x - 9, 354, x + 9, 378), fill=PLUM if i < 2 else BLOCK, outline=CREAM, width=3)
    bar(d, 124, 404, 120)
    bar(d, 412, 404, 120)
    d.rounded_rectangle((124, 470, 532, 560), 14, fill=LIME)
    bar(d, 148, 494, 160, 16, PLUM)
    bar(d, 148, 524, 280, 12, (190, 210, 140))
    d.rounded_rectangle((124, 596, 330, 644), 24, fill=PURPLE)
    card(d, (592, 236, 1422, 676))
    small_label(d, 620, 262, "LEDGER")
    cols = (620, 800, 1090, 1290)
    for x, w in zip(cols, (110, 200, 120, 90)):
        bar(d, x, 300, w, 12, MUTED)
    for r in range(7):
        y = 340 + r * 46
        d.line((620, y - 12, 1394, y - 12), fill=RULE, width=1)
        bar(d, cols[0], y, 120)
        bar(d, cols[1], y, 230 - (r % 3) * 40)
        bar(d, cols[2], y, 90)
        bar(d, cols[3], y, 70, 14, PURPLE if r % 3 else PLUM)
    return im


def content_ship():
    im, d = base("Content Ship", "Internal dashboard · approval and shipping")
    card(d, (96, 236, 330, 676), fill=PLUM)
    for i in range(6):
        d.rounded_rectangle(
            (120, 266 + i * 50, 306 - (i % 2) * 40, 282 + i * 50),
            8,
            fill=(88, 62, 128) if i else LILAC,
        )
    card(d, (356, 236, 900, 676))
    small_label(d, 384, 262, "SCRIPTS")
    states = (LIME, LIME, LILAC, BLOCK, LILAC, BLOCK, LIME)
    for r in range(7):
        y = 300 + r * 52
        d.line((384, y - 10, 872, y - 10), fill=RULE, width=1)
        bar(d, 384, y + 2, 250 - (r % 3) * 46, 14, PLUM)
        bar(d, 384, y + 24, 150)
        d.rounded_rectangle((770, y, 872, y + 28), 14, fill=states[r])
    card(d, (926, 236, 1422, 676))
    small_label(d, 954, 262, "APPROVAL")
    bar(d, 954, 296, 300, 18, PLUM)
    for i in range(4):
        bar(d, 954, 336 + i * 24, 430 - (i % 2) * 90)
    d.rounded_rectangle((954, 448, 1394, 520), 12, fill=BLOCK_ALT)
    d.text((974, 462), "SHA-256", font=text(13, 700), fill=MUTED)
    bar(d, 974, 488, 380, 12, PURPLE)
    d.rounded_rectangle((954, 548, 1160, 596), 24, fill=PURPLE)
    d.rounded_rectangle((1178, 548, 1394, 596), 24, outline=PLUM, width=2)
    bar(d, 954, 628, 260)
    return im


# file name -> (builder, path in the arndvs.com repo)
PLACEHOLDERS = {
    "mcrdse-super-market-placeholder.jpg": (super_market, "public/projects/mcrdse-commerce"),
    "mcrdse-points-ledger-placeholder.jpg": (points_ledger, "public/projects/mcrdse-commerce"),
    "content-ship-placeholder.jpg": (content_ship, "public/projects/mcrdse-content"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate wireframe placeholders.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--site", type=Path, default=None, help="checkout of the arndvs.com repo")
    args = parser.parse_args()

    for name, (build, site_dir) in PLACEHOLDERS.items():
        path = args.out / "placeholders" / name
        save_jpeg(build(), path)
        if args.site:
            dst = args.site / site_dir / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dst)
    if args.site:
        print(f"copied {len(PLACEHOLDERS)} placeholders into {args.site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
