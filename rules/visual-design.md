# Visual Design Rules

Rules for making AI-generated marketing visuals that actually work. These are
the conventions that make a visual legible, shareable, and reusable.

## Legibility

- **One idea per visual.** If you need a second idea, make a second visual.
- **The payoff must land in 3 seconds.** Someone scrolling a feed decides in
  that window whether to keep watching.
- **Text in the frame, not in the audio.** Almost nobody turns sound on in a
  social feed. Every word that matters must be visible.
- **The first frame is the thumbnail.** It has to work as a still, because
  that's all many people will ever see.

## Motion

- **Motion is the explanation, not decoration.** If the animation doesn't
  clarify the idea, cut it.
- **Respect `prefers-reduced-motion`.** Always provide a static fallback.
- **Keep it looping.** A seamless loop makes people watch twice without
  noticing, which counts as more watch time.
- **Don't rush the payoff.** The most common mistake is cutting away before
  the result registers. Hold it.

## Formats

- **4:5 (1080×1350)** — default for LinkedIn/Instagram feeds; takes the most
  screen space on mobile.
- **1:1 (1080×1080)** — square, safe everywhere.
- **16:9 (1920×1080)** — landscape, for YouTube/embed contexts.

## Toolchain

- **Zero dependencies in the output.** The visual file should be
  self-contained HTML/CSS/JS so it embeds anywhere.
- **Document what you used.** Every visual's README lists its toolchain so
  the next one is faster to build.
- **Reuse before you build.** Check `templates/` and existing `visuals/`
  before writing anything new.