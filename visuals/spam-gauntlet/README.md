# The Spam Gauntlet

A stream of identical-looking form submissions runs through seven checks. Junk drops out at each one; one real patient reaches the front desk. Built for the marketing-engineering blog post.

## What it does

- Sixteen "Insurance form" cards enter one after another. They all look the same, which is the point.
- At each of the seven gates (honeypot + timing, rate limit, proxy/VPN, US only, IP blocklist, email check, AI review) some cards turn red, show why ("sent in 0.4 s", "3rd try today · limit 2", "cleaning-service pitch") and get pushed out. Each gate keeps its own count.
- **Payoff:** the one real submission passes all seven, turns green and lands in the front desk inbox. Tally: Blocked 15 · Real 1. Caption: "Seven checks. One real patient."

## Source

AlignSD's 7-layer form protection: honeypot fields with a minimum fill time, per-form rate limits (insurance: 2 per IP per day), IPHub proxy/VPN detection, US-only geo check, a CIDR blocklist, suspicious-email detection, and an OpenAI check that catches sales pitches. The 15-to-1 ratio is illustrative, not a measured rate.

## How it was made

- **Engine:** hand-built HTML/CSS/JS, zero dependencies, Web Animations API. Same frame, controls and fonts as `haskell-to-typescript`.
- **Agent:** Claude, following `.claude/skills/visual-builder` and `rules/visual-design.md`.
- **Toolchain:** Playwright screen capture → ffmpeg for the 4:5 MP4 (one seamless loop, about 18 s).

## Usage

Open `index.html` in any browser. Controls: Run the stream, Restart, Speed, Format (4:5, 1:1, 16:9), Loop, Clean view. Respects `prefers-reduced-motion`.
