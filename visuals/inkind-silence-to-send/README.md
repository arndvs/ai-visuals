# Silence to send

The LinkedIn visual for the first-reward journey post. It opens on a $25 reward and two saved restaurants that get no message for two weeks. Then the four parts of the build light up, and the message lands.

## What it does

- **Hook (0–2.6 s):** the headline names the $25 reward and the two saved spots. The phone shows only a lock screen with no notifications while its date moves from October 14 to October 21 to October 28. The caption says "Two weeks later, nothing had followed up."
- **Build (3.3–5.3 s):** Rails outbox, Snowflake view, Braze profile and Liquid checks light up in order.
- **Payoff (6 s on):** the push arrives ("Your $25 is waiting at Lantern Row"), the headline changes to "Now there's one.", and the test counts appear (184 Liquid, 146 Rails, 11 SQL checks). The payoff holds for about 5 seconds, then the 11.5-second loop restarts.

## How it was made

- **Engine:** hand-built HTML and CSS on the same step timeline as `inkind-message-logic`. No libraries.
- **Palette:** the inKind sample palette from the repo's `ik_brand` tokens. The app in the frame is a generic "Rewards" app, with no inKind logo.
- **Fonts:** Outfit ExtraBold and DM Sans, inlined with `tools/inline-fonts.py`.
- **Render:** `?render=1` exposes `window.renderAt(t)`. It pauses every CSS transition and seeks it, so each frame is exact. Playwright captured 345 frames at 1080×1350 and 30 fps. ffmpeg encoded the MP4 (H.264, CRF 18) and the GIF (720 px wide, 15 fps, 128-colour palette).

## Usage

Open `index.html`. Query options: `?embed=1` hides the controls, `?format=1x1` gives a square frame, `?step=N` freezes on step N (12 is the payoff), and `?loop=0` plays once. Reduced motion shows the payoff as a still.

Files:

- `inkind-silence-to-send-4x5.mp4`, for LinkedIn
- `inkind-silence-to-send-4x5.gif`
- `thumbnail.png`, the first frame

## Credits

Facts and counts come from `arndvs/inkind-first-reward-journey`. All data is fictional, and this is not affiliated with inKind.
