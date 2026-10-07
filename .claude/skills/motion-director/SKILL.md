---
visibility: personal
name: motion-director
description: >
  Router for the motion-graphics toolchain. Use this FIRST for any request to
  create, edit, animate, or render a video, animation, motion graphic, GIF,
  explainer, promo, title card, lower-third, chart animation, or any visual
  output that moves. It decides which engine (HyperFrames, Remotion, GSAP,
  Three.js, Manim, Motion Canvas, Revideo), which renderer, which sound stack,
  and which skill pack to invoke — then hands off to the owning skill. Also
  use it to diagnose why a render failed or to pick the right tool for a
  one-off clip. This is the single entry point; do not guess the stack.
---

# Motion Director

Output "Read Motion Director skill." to chat to acknowledge you read this file.

The motion-graphics toolchain is a **routing layer over installed skills**. You
never guess the stack — you classify the request, then hand off to the owning
skill. This skill is the classifier.

## The toolchain at a glance

| Job | Primary tool | Skill pack | Renderer |
|-----|-------------|------------|----------|
| **Default video from HTML** | HyperFrames | `hyperframes` (entry) + `hyperframes-*` | `npx hyperframes render` → MP4 |
| **React-coded video** | Remotion | `remotion-*` | `npx remotion render` |
| **DOM/SVG animation** | GSAP | `gsap-*` | HyperFrames or browser capture |
| **3D scenes** | Three.js | `threejs-*` | WebGL capture / HyperFrames |
| **Math/diagram animation** | Manim | (Python) | `manim render` |
| **Code explainers (live preview)** | Motion Canvas | (project starter) | `npm init @motion-canvas` |
| **Server-rendered video** | Revideo | (project starter) | `npm init @revideo` |
| **Voiceover / captions** | ElevenLabs + Whisper | `text-to-speech`, `speech-to-text` | — |
| **Music / SFX in code** | Tone.js | (npm) | — |
| **Audio waveforms** | Wavesurfer.js | (npm) | — |
| **Generative art / GIFs** | p5.js | `algorithmic-art`, `canvas-design`, `slack-gif-creator` | — |
| **Blender 3D scenes** | Blender + MCP | `mcp-for-blender` | Blender render |

## Routing rules

Classify the request, then hand off. **Do not skip the owning skill.**

### 1. Video output (MP4/WebM/MOV) — default to HyperFrames

If the user wants a **video file**, the default framework is **HyperFrames**
(renders video from HTML, free per-render, no account). Load `hyperframes`
first — it is the mandatory entry point and routes to the owning workflow
(`motion-graphics`, `general-video`, `product-launch-video`, `pr-to-video`,
`faceless-explainer`, `slideshow`, `talking-head-recut`, `embedded-captions`,
`music-to-video`, `remotion-to-hyperframes`).

- Short design-led unit (<10s, no narration) → `motion-graphics`
- Longer / narrated / multi-scene → `general-video`
- Product/marketing URL → `product-launch-video`
- GitHub PR → `pr-to-video`
- Article/topic explainer → `faceless-explainer`
- Deck/pitch → `slideshow`
- Existing talking-head + graphic overlays → `talking-head-recut`
- Captions only → `embedded-captions`
- Music track → beat-synced video → `music-to-video`
- Existing Remotion project → `remotion-to-hyperframes`

### 2. React-coded video — Remotion

If the user explicitly wants **React code** for the video, or has an existing
Remotion project, use `remotion-*` skills. Remotion is free for individuals
and companies ≤3 people; larger companies need a license.

### 3. DOM/SVG animation — GSAP

If the user wants **web animation** (DOM elements, SVG, scroll-triggered,
timelines) — not a video file — use `gsap-*` skills. GSAP is free including
commercial use. Pair with HyperFrames when the deliverable is a video.

### 4. 3D — Three.js or Blender

- **Web 3D** (scenes, cameras, lighting, shaders) → `threejs-*` skills.
- **Blender 3D** (modeling, rendering, animation) → `mcp-for-blender` MCP
  server (requires Blender installed + `uvx mcp-for-blender install-addon`).

### 5. Math / diagrams — Manim

If the user wants **mathematical animation** (3Blue1Brown style), use Manim
(`pip install manim`, Python 3.11+). Do not install the original 3b1b version
alongside it — the two clash.

### 6. Code explainers — Motion Canvas / Revideo

- **Live preview** while coding → Motion Canvas (`npm init @motion-canvas@latest`).
- **Server-rendered / automated** video → Revideo (`npm init @revideo@latest`).

### 7. Sound

- **Voiceover from text** → `text-to-speech` (ElevenLabs — needs account + API key).
- **Captions from voiceover** → `speech-to-text` (Whisper, local, free; needs ffmpeg).
- **Music / SFX in code** → Tone.js (`npm install tone`).
- **Audio waveforms** → Wavesurfer.js (`npm install wavesurfer.js`).
- **Music / SFX from text** → ElevenLabs `music`, `sound-effects` skills.

### 8. Generative art / GIFs

- **Generative art** (p5.js, flow fields, particles) → `algorithmic-art`.
- **Posters / static designs** → `canvas-design`.
- **Animated GIFs for Slack** → `slack-gif-creator`.

## Render failure diagnosis

When a render fails, do **not** guess. Load the owning skill's CLI reference:

- HyperFrames → `hyperframes-cli` (diagnose build/render failures, `doctor`,
  `check`, `lint`)
- Remotion → `remotion-render` / `remotion-docs`
- Manim → check Python traceback + `manim render --help`

## Toolchain hygiene

- **One engine + one renderer to start.** Do not stack five tools on a first
  clip. The recommended starter pair: GSAP (engine) + HyperFrames (renderer).
- **npm packages** install inside a project folder. **Project starters**
  (Remotion, Motion Canvas, Revideo) create a new folder. **Skills** install
  with `npx skills add`. **MCP servers** connect with `claude mcp add`.
- **Read the README before installing anything.** Each repo runs code on your
  machine. Check the license line for client work (Remotion and react-bits
  both have one worth reading).
- **Commit before installing** so a rollback is instant. Add one at a time.