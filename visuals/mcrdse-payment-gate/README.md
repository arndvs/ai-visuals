# MCRDSE payment gate

An order pipeline where fulfillment waits for an explicit paid status in the database.

## What it does

- A captured payment passes the gate and goes to GoHighLevel and ShipStation.
- A declined capture arrives the same way and stops at the gate.
- Payoff: the unpaid order never reaches fulfillment. 11.5 second loop.

## How it was made

- **Engine:** hand-built HTML and CSS, started from `templates/site-visual.html`. A small step timeline toggles classes; CSS transitions do the motion. No libraries.
- **Palette:** site palette with the MCRDSE project accent (purple), matching its case study.
- **Fonts:** Outfit ExtraBold and DM Sans, inlined with `tools/inline-fonts.py`.

## Usage

Open `index.html` in a browser. Query options:

- `?embed=1` hides the controls (use this in an iframe).
- `?format=16x9`, `4x5` or `1x1` sets the frame.
- `?step=N` freezes on step N for a still. `?loop=0` plays once.

Reduced motion shows the payoff step as a still.

Files: `thumbnail.jpg` (first frame), `still-16x9.jpg` and `still-4x5.jpg` (payoff).

On arndvs.com: `/projects/mcrdse-commerce, in the fail-closed fulfillment section`. Copy it there with `./tools/publish-to-site.sh mcrdse-payment-gate <site repo>`.

## Credits

Based on the MCRDSE commerce case study. Order numbers are illustrative.
