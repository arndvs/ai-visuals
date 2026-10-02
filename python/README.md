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