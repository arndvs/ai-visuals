# Python Helpers

Python utilities for building and post-processing visuals.

## render_loop.py

Renders a looping MP4 from an HTML visual using a headless browser
(Playwright + ffmpeg). Useful when you want a video without screen-recording.

```bash
python python/render_loop.py visuals/haskell-to-typescript/index.html --format 4:5 --out output.mp4
```

Requires: `pip install playwright` + `playwright install chromium`, and ffmpeg.

## make_thumbnail.py

Captures the first frame of a visual as a PNG thumbnail (the frame that works
as a still in a feed).

```bash
python python/make_thumbnail.py visuals/haskell-to-typescript/index.html --out thumbnail.png
```

Requires: `pip install playwright` + `playwright install chromium`.

## site_images/

Generators for the static images on arndvs.com: share cards, blog heroes, and wireframe
placeholders, plus a screenshot cropper. The style rules are in
[`rules/site-images.md`](../rules/site-images.md), and the color and font tokens are in
`site_images/style.py`.

```bash
python python/site_images/generate_cards.py --site ../arndvs
python python/site_images/generate_placeholders.py --site ../arndvs
python python/site_images/crop_screenshot.py capture.jpg out.jpg
```

Output goes to `visuals/arndvs-site-images/`. With `--site`, each image is also copied
to its place in a checkout of the site repo.

Requires: `pip install pillow`. The fonts are bundled in `site_images/fonts`.
