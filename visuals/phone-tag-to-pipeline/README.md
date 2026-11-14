# Phone Tag → Pipeline

Six manual hand-offs to check a new patient's insurance collapse into one upload that routes itself. Built for the marketing-engineering blog post and its LinkedIn launch.

## What it does

- **The old way:** a patient, the front desk and the biller pass calls and emails back and forth ("send us your card", "Fwd: can you verify?", "you're covered"). A counter ticks up to 6 manual hand-offs.
- **The pipeline:** the same three people slide into place and three steps appear between them: upload card + license, the 7-layer spam filter, and an AI read of the card. The packet flows through, routes to the biller as auto-approved, and a confirmation goes back to the patient.
- **Payoff:** the hand-off counter drops to 0. Caption: "One upload. The routing is automatic."
- Routes for "needs review" (front desk) and "spam" (blocked) stay visible but dimmed, so the branching is real, not hidden.

## Source

AlignSD's insurance verification flow: a 5-step form wizard, OpenAI Vision reads the card and license, and confidence decides the route (auto-approve → biller, needs review → front desk, spam → blocked). See `/projects/align-san-diego-family-chiropractic` on arndvs.com.

## How it was made

- **Engine:** hand-built HTML/CSS/JS, zero dependencies. Motion runs on the Web Animations API, with the same frame, controls and fonts as `haskell-to-typescript`.
- **Agent:** Claude, following `.claude/skills/visual-builder` and `rules/visual-design.md`.
- **Toolchain:** Playwright screen capture → ffmpeg for the 4:5 MP4 (one seamless loop, about 27 s).

## Usage

Open `index.html` in any browser. Controls: Play / Restart, Speed, Format (4:5, 1:1, 16:9), Loop, Clean view (`Esc` to exit). Respects `prefers-reduced-motion`.
