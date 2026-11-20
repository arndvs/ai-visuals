# RAG cost levers

Four levers tear strips off a monthly bill for a RAG chatbot: the hero for the RAG Cost Estimator on arndvs.com.

## What it does

- Step 0 (the thumbnail): every lever is up, and the bill is printed at full length: $2,700.00 a month for 10,000 questions a day on Claude Sonnet 5.5.
- Each lever swings over in turn. The strip of paper it saves tears off and falls away, and the total ticks down: $1,755.00, $1,228.50, $1,129.93, $1,020.73.
- The paper is drawn to scale. Each strip's height is its saving's share of $2,700, so the short bill at the end is really 38% of the long one.
- Payoff: "62% less" is stamped where the paper used to be, inside a dashed outline of the original bill marked "Was $2,700.00". 12 second loop; the payoff holds for 4 seconds.

## The figures

Every amount is the estimator's own, for this setup: `/experiments/rag-cost?rs=0.7&hit=0.3&jf=1&fk=2&jg=1` (Claude Sonnet 5.5 main, Claude Haiku 4.5 routed, 10,000 questions a day). The lever chart on that page shows the same steps. If the price table or the estimator changes, check them there and update the totals, the savings, and the strip heights here.

| Lever | Saving | Total after |
|---|---|---|
| None | | $2,700.00 |
| Route 70% to Haiku 4.5 | $945.00 | $1,755.00 |
| Response cache, 30% | $526.50 | $1,228.50 |
| Jev keeps 2 of 8 chunks | $98.57 | $1,129.93 |
| Jev skips unanswerable questions | $109.20 | $1,020.73 |

## How it was made

- **Engine:** hand-built HTML and CSS, started from `templates/site-visual.html`. A step timeline toggles classes; CSS transitions do the motion. No libraries.
- **Palette:** the site's current blue-teal theme (site PR #101): background `#051117`, card `#0A181F`, accent `#2DD4BF`, gradient to `#99F6E4`, and the faint 48px grid from the site's dark body. The template's tokens predate that theme, so this visual overrides them.
- **Fonts:** Bebas Neue, IBM Plex Sans and IBM Plex Mono, the faces the site loads, inlined with `tools/inline-fonts.py`.
- **Formats:** 16:9, 4:5, a 1200×630 share-card frame (`?format=og`), and `?format=card`: the illustration alone, with no headline or captions, for a page that sets its own title beside it.

## Usage

Open `index.html` in a browser. Query options:

- `?embed=1` hides the controls (use this in an iframe).
- `?format=16x9`, `4x5`, `og` or `card` sets the frame.
- `?step=N` freezes on step N for a still. `?loop=0` plays once.

Reduced motion shows the payoff step as a still.

Files: `thumbnail.jpg` (first frame), `still-16x9.jpg` and `still-4x5.jpg` (payoff).

On arndvs.com, two stills of the payoff stand for the experiment: `../arndvs-site-images/experiments/rag-cost-card.jpg` (2400×1350, the `card` frame, on the /experiments card under its own title) and `../arndvs-site-images/share/experiments-rag-cost.jpg` (1200×630, the `og` frame with the headline, for link previews). In the site repo they live at `public/images/experiments/rag-cost-card.jpg` and `public/og/experiments-rag-cost.jpg`.

## Credits

The figures come from the RAG Cost Estimator on arndvs.com. Jev is TypeSafe's decision model; its price comes from TypeSafe's homepage and launch post. Illustration, not a screenshot.
