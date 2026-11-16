# Site Image Rules

Rules for the static images on arndvs.com: share cards, blog heroes, screenshots, and
placeholders. The motion rules in [visual-design.md](visual-design.md) cover animated
visuals; this file covers stills.

The generators in [`python/site_images/`](../python/site_images) implement these rules.
The tokens live in one place, `python/site_images/style.py`. Change a color or a font
there, not in a generator.

## Whose palette

- **The site's own images use the site's palette.** Share cards and blog heroes are
  arndvs.com's voice, so they use arndvs.com's colors and fonts.
- **A piece about another brand may borrow that brand's treatment, and it stays with that
  piece.** The first-reward journey hero uses inKind's gold on plum because the post is
  about inKind. That palette does not carry over to other posts.
- **A placeholder for someone else's screen uses that product's palette.** It stands in
  for a screenshot of their product, so it should sit naturally beside the real ones.

## Colors

Taken from the dark theme in the site's `src/app/globals.css`.

| Role | Value | Token in `style.py` |
|---|---|---|
| Background, share cards | `#0A0A0A` | `BG` |
| Background, blog heroes | `#080808` | `HERO_BG` |
| Accent (the site's `--primary`) | `#2DCCAE` | `ACCENT` |
| Gradient end (the site's `.text-gradient`) | `#B2F5E2` | `ACCENT_END` |
| Headline text | `#FAFAFA` / `#ECECEC` | `WHITE` / `TEXT` |
| Body text | `#A3A3A3` / `#969696` | `GRAY` / `MUTED` |
| Panels and chips | `#121212` / `#141414` | `PANEL` / `CHIP` |
| Hairlines | `#2A2A2A` | `LINE` |
| Passed marks only | `#7EC98E` | `GREEN` |

- Teal is the only accent. Use it for the eyebrow, one highlighted phrase, and one
  filled element in the illustration. It is the same teal as the background of the
  homepage portrait.
- The highlighted phrase in a headline takes the teal-to-mint gradient, the same one
  the site's headings use.
- Green appears only on a check mark that means something passed.

## Fonts

- **Outfit ExtraBold** for headlines.
- **DM Sans** (400, 500, 700) for everything else.
- Both are bundled in `python/site_images/fonts` with their licenses. Do not substitute
  a system font.
- Arrows and check marks are drawn as strokes, because the bundled subsets have no
  symbol glyphs.

## Sizes

| Image | Size | Format |
|---|---|---|
| Share card (link preview) | 1200×630 | JPEG, quality 90 |
| Blog hero | 2400×1350 (16:9) | JPEG, quality 92 |
| Screenshot and placeholder | 1518×759 (2:1) | JPEG, quality 90 |
| LinkedIn banner | 1584×396 | JPEG, quality 92 |

## Share cards

- One per project page, plus the default card for every other page.
- Top to bottom: a short teal rule, an uppercase eyebrow, the title, one sentence, three
  chips, then a footer with the name, the title "Applied AI Full-Stack Engineer", and
  arndvs.com.
- The sentence says what the thing is or what rule it enforces. It is not a slogan.
- The three chips are numbers or named features that appear in the site's facts ledger
  (`docs/reference/facts-ledger.md` in the site repo). Do not put a number on a card
  that is not in the ledger.

## LinkedIn banner

- Same palette, fonts, and headline as the site's homepage, so the profile and the site read
  as one identity.
- The profile photo covers the lower left of the banner, so all text starts at x=470 or
  further right.
- A second banner, the activity grid, has no text. `generate_linkedin_grid.py` draws it from
  real per-day counts in `python/site_images/data/activity-days.json`: one column per week,
  four teal steps by quartile. It is never drawn from made-up data. It is written at double
  size as a PNG (3168×792) so the tiles stay sharp, to
  `visuals/arndvs-site-images/linkedin/banner-activity-grid.png`.
- Written to `visuals/arndvs-site-images/linkedin/banner.jpg`. It is uploaded to LinkedIn
  by hand and is not copied into the site repo.

## Blog heroes

- Left column: eyebrow, a two-line headline with one highlighted phrase, a sentence of up
  to four lines, and up to four topic chips.
- Right column: one panel with one illustration of the post's idea. One idea per image.
- The headline is a short form of the post's claim, not the full title.
- Bottom left carries a one-line note that says what the illustration is. If the image is
  an illustration and not a real screenshot, the note says so.
- No stock photos, no generated photos of people, and no logos of other companies.

## Screenshots

- Capture real pages at a wide viewport, then crop with `crop_screenshot.py` to 2:1.
- Park the cursor at the right edge before capturing, so the crop removes it.
- A caption describes only what is visible in that screenshot.

## Placeholders

- Use one only when the real screen cannot be captured yet (gated or internal).
- Draw a wireframe of the screen's layout in that product's palette, with a
  "Screenshot coming soon" tag. Never ship a card that says "placeholder".
- The file name ends in `-placeholder`, and the caption on the site ends with
  "(screenshot coming soon)". Replace both when the real capture exists.

## Regenerating

```bash
pip install pillow
python python/site_images/generate_cards.py --site ../arndvs
python python/site_images/generate_placeholders.py --site ../arndvs
```

Without `--site`, the images are written to `visuals/arndvs-site-images/` only. With it,
each image is also copied to its place in a checkout of the site repo. Blog heroes land
in `scripts/assets/blog-heroes/` there and go live when `pnpm seed:post-heroes` uploads
them to Sanity.

## Animated visuals for the site

Animated visuals follow `rules/visual-design.md` and these additions.

- **Start from `templates/site-visual.html`** (`./tools/new-visual.sh <name> --site`). It carries the site palette, the fonts, the motion tokens and the step timeline.
- **Motion tokens:** `--fast` 180ms, `--base` 420ms, `--slow` 760ms, one easing (`--ease`). Don't add other durations or easings.
- **Length:** a loop of 12 seconds or less. Hold the payoff for at least 2.5 seconds.
- **Step 0 is the thumbnail.** Every element is on screen in its idle state. Steps change state; they don't reveal the layout.
- **Reduced motion** shows the payoff step (`STILL`) with no transitions.
- **Colour:** site teal by default. A case study's visual uses that project's accent. A visual for a post about another brand uses that brand's sample palette and nothing from the site but the fonts.
- **Captions state what is on screen.** No claim in a caption that isn't on the page it supports.
- **Ship three stills** with each visual: `thumbnail.jpg`, `still-16x9.jpg`, `still-4x5.jpg`.
- **Inline the fonts** before publishing (`tools/inline-fonts.py`), then copy to the site (`tools/publish-to-site.sh`).
