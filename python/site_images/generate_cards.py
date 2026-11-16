#!/usr/bin/env python3
"""generate_cards.py — share cards, blog heroes and the LinkedIn banner, in the site's own style.

Share cards are 1200x630 link previews: one default card and one per project page.
Blog heroes are 2400x1350 title cards for posts that have no image of their own.

Usage:
    python python/site_images/generate_cards.py [--out DIR] [--site PATH_TO_ARNDVS_REPO]

--out   where to write (default: visuals/arndvs-site-images)
--site  also copy each image to its place in a checkout of the arndvs.com repo

To add a card, add an entry to SHARE_CARDS. To add a hero, add a function like
hero_tailwind() and call it from main(). Follow rules/site-images.md.

Requires: pip install pillow.
"""

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from style import (
    ACCENT,
    ACCENT_END,
    BAR,
    BG,
    BLOCK,
    BLOCK_ALT,
    CHIP,
    DEFAULT_OUT,
    DIM,
    GLOW,
    GRAY,
    GREEN,
    HERO_BG,
    LINE,
    MUTED,
    NOTE,
    PANEL,
    SOFT,
    TEXT,
    WHITE,
    arrow_down,
    check,
    chips,
    display,
    gradient_text,
    save_jpeg,
    spaced,
    text,
    wrap,
)

# ---------------------------------------------------------------- share cards

# slug -> (eyebrow, title, one line, three chips). Numbers come from the site's facts ledger.
SHARE_CARDS = {
    "og-image": (
        "Applied AI Full-Stack Engineer",
        "Aaron Davis",
        "I build AI features and the systems around them, from discovery to production.",
        ["Agents and RAG", "Marketing automation", "TypeScript · Python"],
    ),
    "inkind-first-reward-journey": (
        "Lifecycle marketing · Work sample",
        "First-Reward Journey",
        "The message a rewards app should have sent me, built end to end. Not affiliated with inKind.",
        ["184 Liquid tests", "146 Rails tests", "11/11 SQL checks"],
    ),
    "ctrlshft": (
        "AI agent infrastructure · Open source",
        "ctrl+shft",
        "Skills, guardrail hooks and a sandboxed loop that keep AI coding agents consistent and safe.",
        ["50+ skills", "19 guardrail hooks", "3 AI runtimes"],
    ),
    "ripemetrics": (
        "Marketing automation · AI platform · 2017–2025",
        "RipeMetrics",
        "The customer growth platform I co-founded and built on for 8 years.",
        ["21 journey triggers", "38 segmentation scopes", "RAG across 4 channels"],
    ),
    "align-san-diego-family-chiropractic": (
        "Healthcare platform · 2025–2026",
        "Align San Diego",
        "A clinic platform with AI insurance verification, built solo on Next.js and Sanity.",
        ["5 AI integrations", "5,000+ families served", "12+ integrations"],
    ),
    "mcrdse-commerce": (
        "E-commerce · Loyalty · Edge computing",
        "MCRDSE Commerce",
        "An order pipeline where nothing ships until the database confirms payment.",
        ["284 audit items closed", "195 tests, from none", "580 orders recovered"],
    ),
    "mcrdse-content": (
        "Content operations · AI search",
        "MCRDSE Content",
        "Approval locked to a content hash, so an edited draft can't ship as approved.",
        ["Content-hash approval", "Human sign-off", "Archetype quiz"],
    ),
    "push": (
        "AI video · Short film · In progress",
        "PUSH",
        "A comedy short about a man, a hangover, and a mechanical bed with no off switch.",
        ["55-shot prompt library", "17 production docs", "Screenplay v7"],
    ),
    "rise-awake": (
        "Creative technology · Full-stack web",
        "RISE Awake",
        "The real corporate website of a fictional company that sells push beds.",
        ["41 routes", "22 internal docs", "6 legal docs"],
    ),
}


def share_card(eyebrow, title, sub, tags):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(glow).ellipse((720, -260, 1460, 480), fill=GLOW)
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(140)), 0.9)
    d = ImageDraw.Draw(im)
    d.rectangle((80, 78, 128, 84), fill=ACCENT)
    spaced(d, (80, 108), eyebrow.upper(), text(21, 500), ACCENT, 3.2)
    tf = display(92)
    if d.textlength(title, font=tf) > W - 160:
        tf = display(76)
    d.text((76, 152), title, font=tf, fill=WHITE)
    sf = text(32)
    y = 152 + tf.size + 42
    for line in wrap(d, sub, sf, W - 220)[:2]:
        d.text((80, y), line, font=sf, fill=GRAY)
        y += 46
    chips(d, 80, 448, tags, text(22, 500), 22, 48, 14, CHIP, DIM, WHITE)
    d.line((80, 540, W - 80, 540), fill=DIM, width=1)
    nf = text(24, 500)
    d.text((80, 562), "Aaron Davis", font=nf, fill=WHITE)
    x = 80 + d.textlength("Aaron Davis", font=nf) + 14
    d.text((x, 562), "·  Applied AI Full-Stack Engineer", font=text(24), fill=GRAY)
    uf = text(24, 500)
    d.text((W - 80 - d.textlength("arndvs.com", font=uf), 562), "arndvs.com", font=uf, fill=ACCENT)
    return im


# ---------------------------------------------------------------- LinkedIn banner


def linkedin_banner():
    """1584x396 profile banner. The profile photo covers the lower left, so text starts at x=470."""
    W, H = 1584, 396
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(glow).ellipse((900, -300, 1800, 520), fill=GLOW)
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(150)), 0.95)
    d = ImageDraw.Draw(im)
    x = 470
    d.rectangle((x, 66, x + 48, 72), fill=ACCENT)
    spaced(d, (x, 92), "APPLIED AI FULL-STACK ENGINEER", text(20, 500), ACCENT, 3.2)
    # Largest size up to 56px at which the whole headline fits before the right margin.
    size = 56
    while size > 36 and d.textlength("I build AI features and the systems around them", font=display(size)) > W - x - 72:
        size -= 1
    tf = display(size)
    d.text((x - 3, 132), "I build AI features", font=tf, fill=WHITE)
    w = d.textlength("I build AI features ", font=tf)
    gradient_text(im, (x - 3 + w, 132), "and the systems around them", tf, ACCENT, ACCENT_END)
    d = ImageDraw.Draw(im)
    d.text(
        (x, 222),
        "Agents, RAG and lifecycle marketing infrastructure, built with the people who use them.",
        font=text(24),
        fill=GRAY,
    )
    chips(
        d,
        x,
        290,
        ["Agents and RAG", "Marketing automation", "Braze and Snowflake certified"],
        text(20, 500),
        20,
        44,
        12,
        CHIP,
        DIM,
        WHITE,
    )
    uf = text(22, 500)
    d.text((W - 72 - d.textlength("arndvs.com", font=uf), 300), "arndvs.com", font=uf, fill=ACCENT)
    return im


# ---------------------------------------------------------------- blog heroes

S = 1.5  # heroes are laid out on a 1600x900 grid and drawn at 1.5x


def px(v):
    return int(round(v * S))


def hero_base(eyebrow, line1, line2, highlight, sub, tags, note):
    """Left column of a blog hero. Words in `highlight` take the teal-to-mint gradient."""
    W, H = px(1600), px(900)
    im = Image.new("RGB", (W, H), HERO_BG)
    glow = Image.new("RGB", (W, H), HERO_BG)
    ImageDraw.Draw(glow).ellipse((px(900), px(120), px(1650), px(820)), fill=GLOW)
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(px(120))), 0.85)
    d = ImageDraw.Draw(im)
    spaced(d, (px(112), px(190)), eyebrow.upper(), text(px(20), 700), ACCENT, px(5.4))
    size = 104
    tf = display(px(size))
    while max(d.textlength(line1, font=tf), d.textlength(line2, font=tf)) > px(740):
        size -= 2
        tf = display(px(size))
    y = px(250)
    for line in (line1, line2):
        x = px(108)
        for word in line.split():
            if word in highlight:
                gradient_text(im, (x, y), word, tf, ACCENT, ACCENT_END)
            else:
                d.text((x, y), word, font=tf, fill=TEXT)
            x += d.textlength(word + " ", font=tf)
        y += px(size * 1.08)
    sf = text(px(30))
    y += px(34)
    for line in wrap(d, sub, sf, px(680))[:4]:
        d.text((px(112), y), line, font=sf, fill=MUTED)
        y += px(43)
    chips(d, px(112), y + px(26), tags, text(px(20), 500), px(21), px(46), px(12), CHIP, LINE, TEXT)
    d.text((px(112), px(836)), note, font=text(px(16)), fill=NOTE)
    return im, d


def panel(d, box=(930, 150, 1490, 750)):
    d.rounded_rectangle([px(v) for v in box], px(28), fill=PANEL, outline=LINE, width=px(2))


def bar(d, x, y, w, h=14, fill=BAR):
    d.rounded_rectangle((px(x), px(y), px(x + w), px(y + h)), px(h / 2), fill=fill)


def label(d, x, y, s, fill=SOFT):
    d.text((px(x), px(y)), s, font=text(px(15), 700), fill=fill)


def tiles(d, x, y, letters, size, gap, fill, text_fill, outline=None):
    f = text(px(size * 0.5), 700)
    for ch in letters:
        d.rounded_rectangle(
            (px(x), px(y), px(x + size), px(y + size)), px(12), fill=fill, outline=outline, width=px(2)
        )
        w = d.textlength(ch, font=f)
        d.text((px(x + size / 2) - w / 2, px(y + size * 0.2)), ch, font=f, fill=text_fill)
        x += size + gap


def hero_readable_vs_explainable():
    im, d = hero_base(
        "Agents, types and verification",
        "We stop reading",
        "every line",
        {"every", "line"},
        "Take the human out of the reading seat and readability stops being the goal. "
        "What replaces it is something you can check.",
        ["Haskell", "TypeScript", "Types", "Agents"],
        "The example in the post: obfuscated Haskell that turned out to be bubble sort.",
    )
    panel(d)
    label(d, 968, 186, "UNREADABLE")
    for i, w in enumerate([420, 300, 380, 240, 340]):
        bar(d, 968, 226 + i * 30, w)
    d.line((px(968), px(396), px(1452), px(396)), fill=LINE, width=px(2))
    label(d, 968, 424, "RUN IT")
    tiles(d, 968, 464, "banana", 62, 12, BLOCK, TEXT, LINE)
    arrow_down(d, px(1190), px(548), px(34), ACCENT)
    tiles(d, 968, 610, "aaabnn", 62, 12, ACCENT, HERO_BG)
    check(d, px(968), px(700), px(18), GREEN)
    d.text((px(998), px(696)), "sorted, so I believe the explanation", font=text(px(17), 500), fill=GREEN)
    return im


def hero_programming_as_theory_building():
    im, d = hero_base(
        "Peter Naur, 1985",
        "The real product",
        "isn't the code",
        {"the", "code"},
        "A program's most important product is the theory in the programmer's mind. "
        "AI can write code without building one.",
        ["Programming", "AI", "Software Engineering"],
        "After Peter Naur, Programming as Theory Building.",
    )
    panel(d)
    label(d, 968, 186, "THEORY", ACCENT)
    d.text((px(968), px(212)), "why the code is the way it is", font=text(px(19)), fill=MUTED)
    x0, y0, x1, y1, dash, gap = 968, 262, 1452, 712, 16, 12
    x = x0
    while x < x1:
        for y in (y0, y1):
            d.line((px(x), px(y), px(min(x + dash, x1)), px(y)), fill=ACCENT, width=px(3))
        x += dash + gap
    y = y0
    while y < y1:
        for x in (x0, x1):
            d.line((px(x), px(y), px(x), px(min(y + dash, y1))), fill=ACCENT, width=px(3))
        y += dash + gap
    for i, t in enumerate(["what the business needs", "what was tried and dropped", "what must never change"]):
        d.text((px(1000), px(292 + i * 34)), "·  " + t, font=text(px(18)), fill=MUTED)
    d.rounded_rectangle(
        (px(1100), px(440), px(1320), px(672)), px(16), fill=BLOCK, outline=LINE, width=px(2)
    )
    label(d, 1124, 462, "CODE", TEXT)
    for i, w in enumerate([150, 110, 170, 90, 130, 100]):
        bar(d, 1124, 502 + i * 26, w, 12, SOFT)
    return im


def hero_tailwind_indicator():
    im, d = hero_base(
        "Open source · npm",
        "Know your",
        "breakpoint",
        {"breakpoint"},
        "A 4 KB, zero-dependency Web Component that shows the Tailwind breakpoint "
        "you're targeting while you build.",
        ["Tailwind CSS", "Web Components", "TypeScript", "npm"],
        "Illustration of the indicator badge on a page layout.",
    )
    panel(d)
    for i, c in enumerate([(236, 106, 94), (244, 191, 79), (98, 197, 84)]):
        d.ellipse((px(962 + i * 26), px(180), px(978 + i * 26), px(196)), fill=c)
    d.rounded_rectangle((px(1060), px(174), px(1452), px(202)), px(14), fill=BLOCK)
    d.line((px(930), px(226), px(1490), px(226)), fill=LINE, width=px(2))
    d.rounded_rectangle((px(968), px(258), px(1452), px(400)), px(14), fill=BLOCK)
    for i in range(3):
        x = 968 + i * 166
        d.rounded_rectangle(
            (px(x), px(426), px(x + 152), px(560)), px(14), fill=BLOCK_ALT, outline=LINE, width=px(2)
        )
        bar(d, x + 18, 446, 92, 12, SOFT)
        bar(d, x + 18, 472, 62, 10)
    bar(d, 968, 586, 332)
    bar(d, 968, 614, 232)
    bf = text(px(22), 700)
    badge = "lg  ·  1280 × 720"
    bw = d.textlength(badge, font=bf) + px(40)
    d.rounded_rectangle((px(962), px(676), px(962) + bw, px(726)), px(25), fill=ACCENT)
    d.text((px(962) + px(20), px(687)), badge, font=bf, fill=HERO_BG)
    return im


def hero_sanity_content_ops():
    im, d = hero_base(
        "Sanity · Next.js · AI",
        "Production Sanity,",
        "AI content ops",
        {"AI", "content", "ops"},
        "Schema design, an Enhance action that returns validated output, "
        "and revalidation that keeps content live in seconds.",
        ["Sanity", "Next.js", "AI", "SEO"],
        "Illustration of an editor's Enhance action filling validated fields.",
    )
    panel(d)
    label(d, 968, 186, "DOCUMENT")
    d.rounded_rectangle((px(968), px(222), px(1300), px(244)), px(10), fill=TEXT)
    for i, w in enumerate([470, 430, 380]):
        bar(d, 968, 268 + i * 26, w, 12)
    ef = text(px(20), 700)
    ew = d.textlength("Enhance", font=ef) + px(48)
    d.rounded_rectangle((px(968), px(370), px(968) + ew, px(422)), px(26), fill=ACCENT)
    d.text((px(968) + px(24), px(383)), "Enhance", font=ef, fill=HERO_BG)
    d.line((px(968), px(456), px(1452), px(456)), fill=LINE, width=px(2))
    rows = [("SEO title", 300), ("Meta description", 360), ("Focus keyword", 180), ("Structured data", 250)]
    for i, (name, w) in enumerate(rows):
        y = 486 + i * 58
        d.text((px(968), px(y)), name, font=text(px(17), 500), fill=MUTED)
        bar(d, 968, y + 28, w, 12, SOFT)
        check(d, px(1424), px(y + 14), px(20), GREEN)
    return im


# post slug -> hero
BLOG_HEROES = {
    "readable-vs-explainable": hero_readable_vs_explainable,
    "programming-as-theory-building": hero_programming_as_theory_building,
    "tailwind-indicator": hero_tailwind_indicator,
    "building-production-sanity-cms-ai-content-ops": hero_sanity_content_ops,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate arndvs.com share cards and blog heroes.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--site", type=Path, default=None, help="checkout of the arndvs.com repo")
    args = parser.parse_args()

    copies = []
    for slug, spec in SHARE_CARDS.items():
        path = args.out / "share" / f"{slug}.jpg"
        save_jpeg(share_card(*spec), path)
        site_rel = "public/images/og-image.jpg" if slug == "og-image" else f"public/og/{slug}.jpg"
        copies.append((path, site_rel))
    for slug, build in BLOG_HEROES.items():
        path = args.out / "blog-heroes" / f"{slug}.jpg"
        save_jpeg(build(), path, quality=92)
        copies.append((path, f"scripts/assets/blog-heroes/{slug}.jpg"))

    save_jpeg(linkedin_banner(), args.out / "linkedin" / "banner.jpg", quality=92)

    if args.site:
        for src, rel in copies:
            dst = args.site / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        print(f"copied {len(copies)} images into {args.site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
