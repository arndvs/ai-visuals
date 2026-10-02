# Tools

Scripts and utilities used to build and ship visuals.

## render-to-mp4.sh

Renders an HTML visual to MP4 using HyperFrames.

```bash
./tools/render-to-mp4.sh visuals/haskell-to-typescript/index.html
```

Requires the HyperFrames CLI (`npx skills add heygen-com/hyperframes`).

## serve.sh

Serves the repo locally so you can preview visuals before shipping.

```bash
./tools/serve.sh
```

Then open `http://localhost:8000/visuals/<name>/`.

## new-visual.sh

Scaffolds a new visual folder from the template.

```bash
./tools/new-visual.sh my-new-visual
```

Creates `visuals/my-new-visual/` with `index.html` and `README.md` from
`templates/`.