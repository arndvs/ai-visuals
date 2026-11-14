"""Shared style for arndvs.com static images. The rules are in rules/site-images.md.

Colors mirror the dark theme in the site's src/app/globals.css. Fonts are the faces the
site loads: Outfit for display, DM Sans for text. Both are bundled in ./fonts.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FONTS = HERE / "fonts"
DEFAULT_OUT = REPO / "visuals" / "arndvs-site-images"

# Site palette (dark theme)
BG = (10, 10, 10)  # share-card background
HERO_BG = (8, 8, 8)  # blog-hero background
ORANGE = (255, 121, 42)  # --primary, and the start of .text-gradient
AMBER = (255, 193, 7)  # the end of .text-gradient
WHITE = (250, 250, 250)
TEXT = (236, 236, 236)
GRAY = (163, 163, 163)
MUTED = (150, 150, 150)
NOTE = (110, 110, 110)
PANEL = (18, 18, 18)
CHIP = (20, 20, 20)
LINE = (42, 42, 42)
DIM = (38, 38, 38)
BAR = (50, 50, 50)
BLOCK = (30, 30, 30)
BLOCK_ALT = (24, 24, 24)
SOFT = (76, 76, 76)
GLOW = (46, 24, 10)  # blurred orange glow behind the right-hand side
GREEN = (126, 201, 142)  # "passed" marks only


def display(size):
    """Outfit ExtraBold: headlines."""
    return ImageFont.truetype(str(FONTS / "Outfit-ExtraBold.woff"), int(size))


def text(size, weight=400):
    """DM Sans: everything that is not a headline. weight is 400, 500 or 700."""
    return ImageFont.truetype(str(FONTS / f"DMSans-{weight}.woff"), int(size))


def spaced(d, xy, s, f, fill, spacing):
    """Letterspaced text, for uppercase eyebrows."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing
    return x


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chips(d, x, y, items, f, pad_x, h, gap, fill, outline, text_fill):
    for item in items:
        w = d.textlength(item, font=f) + pad_x * 2
        d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=fill, outline=outline, width=2)
        d.text((x + pad_x, y + (h - f.size) / 2 - f.size * 0.12), item, font=f, fill=text_fill)
        x += w + gap


def gradient_text(im, xy, s, f, c0=ORANGE, c1=AMBER):
    """The site's .text-gradient: orange to amber across the word."""
    d = ImageDraw.Draw(im)
    left, top, right, bottom = (int(v) for v in d.textbbox(xy, s, font=f))
    right, bottom = right + 2, bottom + 2
    w, h = max(right - left, 1), max(bottom - top, 1)
    grad = Image.new("RGB", (w, h))
    gp = grad.load()
    for x in range(w):
        for y in range(h):
            k = min(1.0, max(0.0, (x / w + y / h) / 2))
            gp[x, y] = tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).text(xy, s, font=f, fill=255)
    im.paste(grad, (left, top), mask.crop((left, top, right, bottom)))


def check(d, x, y, size, fill):
    """A check mark drawn as a stroke, so no symbol font is needed."""
    w = max(2, int(size * 0.16))
    d.line(
        [(x, y + size * 0.55), (x + size * 0.36, y + size * 0.88), (x + size, y + size * 0.14)],
        fill=fill,
        width=w,
        joint="curve",
    )


def arrow_down(d, x, y, size, fill):
    w = max(2, int(size * 0.14))
    cx = x + size / 2
    d.line([(cx, y), (cx, y + size)], fill=fill, width=w)
    d.line(
        [(cx - size * 0.32, y + size * 0.64), (cx, y + size), (cx + size * 0.32, y + size * 0.64)],
        fill=fill,
        width=w,
        joint="curve",
    )


def save_jpeg(im, path, quality=90):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=quality, optimize=True)
    print(f"wrote {path.relative_to(REPO) if path.is_relative_to(REPO) else path}")
