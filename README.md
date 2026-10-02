# AI Visuals Hub

A home for AI-generated marketing visuals — the rules, tools, skills, and
templates used to create them, plus the outputs themselves.

The idea: when a complex idea is hard to hold in your head, a few seconds of
well-designed motion can compress a page of reasoning into something you
instantly get. This repo is where those visuals live, and where the machinery
to make more of them is kept.

## Layout

```
ai-visuals/
├── visuals/          ← The outputs. One folder per visual.
│   └── haskell-to-typescript/
│       ├── index.html    ← the animation (self-contained, zero deps)
│       └── README.md     ← what it is, how it was made
├── rules/            ← Design rules and conventions for making visuals
├── tools/            ← Scripts and utilities used to build visuals
├── skills/           ← Agent skills that encode the craft
├── python/           ← Python helpers (rendering, post-processing)
└── templates/        ← Reusable starting points for new visuals
```

## How to add a new visual

1. **Copy a template** — start from `templates/` rather than a blank file.
2. **Build it** — use the tools and skills in this repo; follow the rules.
3. **Document it** — every visual gets a `README.md` in its folder: what it
   shows, how it was made, what toolchain it used.
4. **Ship it** — the visual is served from GitHub Pages at
   `https://arndvs.github.io/ai-visuals/<visual-name>/`.

## The toolchain

Built with the motion-graphics skill stack:

- **HyperFrames** — renders an HTML page to MP4 (free, no account)
- **GSAP / Remotion / Three.js skill packs** — motion reference and patterns
- **ffmpeg** — video post-work (cut, join, convert)
- **Web Animations API** — the animations themselves stay dependency-free so
  they embed anywhere

## License

MIT