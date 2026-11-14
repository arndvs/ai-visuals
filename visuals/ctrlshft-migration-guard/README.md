# ctrl+shft migration guard

A PreToolUse hook that blocks a database migration unless it targets a test database.

## What it does

- The agent asks to run `npx prisma migrate deploy`.
- `migration-guard.sh` exits 2 and the command never runs.
- Payoff: with a test `DATABASE_URL` the same command is allowed. 11.5 second loop.

## How it was made

- **Engine:** hand-built HTML and CSS, started from `templates/site-visual.html`. A small step timeline toggles classes; CSS transitions do the motion. No libraries.
- **Palette:** site palette (teal).
- **Fonts:** Outfit ExtraBold and DM Sans, inlined with `tools/inline-fonts.py`.

## Usage

Open `index.html` in a browser. Query options:

- `?embed=1` hides the controls (use this in an iframe).
- `?format=16x9`, `4x5` or `1x1` sets the frame.
- `?step=N` freezes on step N for a still. `?loop=0` plays once.

Reduced motion shows the payoff step as a still.

Files: `thumbnail.jpg` (first frame), `still-16x9.jpg` and `still-4x5.jpg` (payoff).

On arndvs.com: `/projects/ctrlshft, in Lifecycle Hooks`. Copy it there with `./tools/publish-to-site.sh ctrlshft-migration-guard <site repo>`.

## Credits

Simplified from `hooks/migration-guard.sh` in `arndvs/ctrlshft`. The real hook prints a JSON deny reason.
