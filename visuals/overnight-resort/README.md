# The Overnight Re-sort

Every customer gets re-scored overnight; only the ones who changed get sent to the CRM. Built for the marketing-engineering blog post and its LinkedIn series.

## What it does

- Customers sit as dots in six lifecycle columns: New, Active, VIP, At-risk, Lapsed, Dormant, each with its real rule (for example "2+ orders · ≤90 days").
- **Nightly run:** a scan sweeps every column (everyone re-scored), then a handful of customers arc into a new column and one first-time buyer appears.
- **Payoff:** only those few fly into the GoHighLevel box, which logs the tag changes (`lifecycle-at-risk → lifecycle-lapsed`). Counter: "Sent to the CRM: 7 of 65 re-scored". Caption: "Only the changes get sent."
- The loop runs night after night with different moves (seeded, so it's repeatable).

## Source

MCRDSE's segment engine: a nightly Cloudflare Worker that classifies every buyer from D1 (`classifyLifecycle`), diffs against `segment_sync_state`, and only writes changed contacts to GHL. Stage rules in the visual match the code.

## How it was made

- **Engine:** hand-built HTML/CSS/JS, zero dependencies, Web Animations API (FLIP-style re-layout). Same frame, controls and fonts as `haskell-to-typescript`.
- **Agent:** Claude, following `.claude/skills/visual-builder` and `rules/visual-design.md`.
- **Toolchain:** Playwright screen capture → ffmpeg for the 4:5 MP4 (two nights, about 25 s).

## Usage

Open `index.html` in any browser. Controls: Run tonight / Next day, Restart, Speed, Format (4:5, 1:1, 16:9), Loop, Clean view. Respects `prefers-reduced-motion`.
