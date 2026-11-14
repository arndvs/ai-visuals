# inKind message logic

A Braze message that reads the reward off the profile before it renders, and aborts with a reason when the data is wrong.

## What it does

- Test user A ($25 reward) passes four checks and the message sends.
- Test user B (zero reward) fails the second check.
- Payoff: `abort_message("reward amount is zero")`, nothing sent. 12 second loop.

## How it was made

- **Engine:** hand-built HTML and CSS, started from `templates/site-visual.html`. A small step timeline toggles classes; CSS transitions do the motion. No libraries.
- **Palette:** the inKind sample palette from the repo's `ik_brand` tokens (dark `#1b151e`, gold `#E7B84B`). This visual belongs to a post about another brand, so it does not use the site palette.
- **Fonts:** Outfit ExtraBold and DM Sans, inlined with `tools/inline-fonts.py`.

## Usage

Open `index.html` in a browser. Query options:

- `?embed=1` hides the controls (use this in an iframe).
- `?format=16x9`, `4x5` or `1x1` sets the frame.
- `?step=N` freezes on step N for a still. `?loop=0` plays once.

Reduced motion shows the payoff step as a still.

Files: `thumbnail.jpg` (first frame), `still-16x9.jpg` and `still-4x5.jpg` (payoff).

On arndvs.com: `/projects/inkind-first-reward-journey, in The Message`. Copy it there with `./tools/publish-to-site.sh inkind-message-logic <site repo>`.

## Credits

Attribute names and abort reasons come from `arndvs/inkind-first-reward-journey`. Fictional data. Not affiliated with inKind.
