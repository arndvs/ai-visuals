# Skills

Agent skills that encode the craft of making AI-generated visuals. Each skill
is a self-contained workflow an agent can follow.

## visual-builder

The core skill: given a concept, produce a self-contained HTML visual that
explains it in motion.

**Input:** a concept, a target format (4:5 / 1:1 / 16:9), and any source
material (code, data, text).

**Output:** a single `index.html` with zero external dependencies, plus a
`README.md` documenting the toolchain.

**Process:**

1. **Understand** — read the source material until you can explain it to a
   child. If you can't, neither can the visual.
2. **Design** — pick the one idea, the payoff, and the loop. Sketch the
   frames before writing code.
3. **Build** — write the HTML/CSS/JS. Motion on the Web Animations API.
   Respect `prefers-reduced-motion`.
4. **Verify** — open it, watch the loop twice, check the first frame works
   as a still.
5. **Document** — write the README: what it shows, how it was made, what
   toolchain it used.

## Rules to follow

- One idea per visual.
- The payoff lands in 3 seconds.
- Text in the frame, not in audio.
- First frame works as a thumbnail.
- Motion is the explanation, not decoration.
- Zero dependencies in the output.