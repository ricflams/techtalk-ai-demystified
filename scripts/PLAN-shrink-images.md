# Plan: shrink `src/images` without visible quality loss at HD

## Context

`src/images` is **276.6 MB across 265 files**, and every one of them is referenced from
`src/slides.md` (255 `<img>` tags + 15 `![bg]` markers). Marp emits one HTML file
containing every slide, so opening `presentation.html` pulls the whole 277 MB — that is
what makes the deployed GitHub Pages deck slow to load.

The weight is almost entirely **excess pixel dimensions**, not bad compression:

| | files | bytes |
|---|---|---|
| Larger than 1920×1080 | 181 | 239.9 MB |
| Already within 1920×1080 | 72 | 35.2 MB |
| SVG (left alone) | 12 | 1.5 MB |

Typical offenders are 3168×1344 and 2816×1536 screenshots and AI illustrations. The Marp
canvas is **1280×720 CSS px** (no `size:` directive anywhere, so Marp's default applies),
so fullscreen on an HD display the deck renders at exactly **1.5×** — a 1920×1080 source
is the precise point where additional pixels stop being visible. There are no duplicate
files and only 3 unreferenced ones, so dedup is not the lever.

**Goal:** the largest possible size reduction with *no* quality reduction visible at HD.
Stay on PNG (and SVG); no WebP conversion.

## Approach

Two levers, both safe:

1. **Downscale to fit a 1920×1080 box.** Single uniform scale factor
   `min(1920/w, 1080/h, 1.0)` — so aspect ratio is never altered and images already at or
   below the box are never upscaled or re-encoded larger. This is where the bulk of the
   saving comes from.
2. **Lossless re-encode.** Bit-exact pixel output: drop a fully-opaque alpha channel,
   use an exact palette when an image genuinely has ≤256 colours, then run `oxipng` at
   max effort. Never changes a single pixel value.

Measured outcome of lever 1 + Pillow-only encoding: **276.6 MB → 151.8 MB (−45%)**.
Adding `oxipng -o max` typically yields another 10–25%, so expect roughly **120–140 MB**.

### Honest caveat

Downscaling is the only step that alters pixels. It is invisible at HD and in a
screen-shared call, which is what you asked for. If you ever present fullscreen on a
**4K** display the canvas scales 3×, and these images would then be upscaled by the
browser and look softer than today. That is the accepted trade of choosing the HD ceiling.

## Implementation

### New file: `scripts/shrink_images.py`

A standalone one-shot tool (also reusable when new screenshots are added later). Modelled
on the existing `scripts/*.py` style — plain stdlib + Pillow, no framework.

Per file under `src/images`:

- **`.svg`** → untouched. (12 files, 1.5 MB; not worth a new `svgo` dependency.)
- **Alpha** → convert `RGBA`/`P` to `RGB` only when the alpha channel is fully opaque.
  A uniformly-opaque alpha channel carries no information, so this is bit-exact.
- **Resize** → `scale = min(1920/w, 1080/h, 1.0)`; skip entirely when `scale == 1.0`.
  Resample with `Image.LANCZOS`.
- **PNG encode** → `optimize=True`; additionally try an exact adaptive palette when
  `im.getcolors(256)` is non-empty, verified bit-identical via `ImageChops.difference`,
  and keep whichever is smaller.
- **JPEG / WebP sources** (13 files) → keep their format. Byte-copy when already within
  the box; only `intro/books.jpg` (3791×2050) and `bonus/cost/harry-potter-page-1.jpg`
  (3024×4032) actually need resizing, re-encoded at quality 92 with 4:4:4 subsampling.
- **Never grow a file** → if the candidate output is larger than the source and the source
  was already within the box, keep the source bytes.

Then run `oxipng` over every written PNG:

```python
oxipng.optimize(path, level=6, strip=oxipng.StripChunks.safe)
```

New dependency: `pip install pillow pyoxipng` (Pillow 12.3.0 is already present;
`pyoxipng` is not yet installed).

### Files touched

- `scripts/shrink_images.py` — new.
- `src/images/**` — rewritten in place. No path or filename changes, so **`src/slides.md`
  needs no edits at all**.
- `CLAUDE.md` — add a short note under Build describing the script and the 1920×1080
  convention for new screenshots.
- `scripts/README.md` — one entry, matching how the other scripts are listed there.

### Safety

Commit the current state on a branch **before** running, so every original is recoverable
from git history. The script writes in place, so this is the only rollback path.

## Verification

1. **Invariant check** (fail the run if violated): for every file, output width ≤ input
   width, output height ≤ input height, output ≤ 1920×1080, and
   `|out_w/out_h − in_w/in_h| / (in_w/in_h) < 0.005` (rounding tolerance only). No
   upscales, no aspect-ratio drift.
2. **Bit-exactness of the non-resize steps**: for files already within the box, assert the
   decoded pixels are identical to the original before/after.
3. **Report** total before/after and the 20 largest remaining files.
4. **Rebuild the deck** with the documented command chain and confirm it still builds:

   ```bash
   marp src/slides.md --html --theme src/marp-theme.css --output public/presentation.html
   cp -r src/images public/images && cp src/layout.css public/layout.css
   python scripts/make_readable.py src/slides.md public/index.html
   python scripts/make_notes.py src/slides.md public/presentation.html public/notes.json
   ```

5. **Visual spot-check at HD**: open `public/presentation.html` fullscreen on the 1080p
   display and step through the slides carrying the most aggressively downscaled images —
   `overview/*.png` (3168×1344 → 1920×815), `llm/nerdflix.png`, `intro/dopamine.png`,
   `intro/journey/enter-rabbithole.png`, and the dense text screenshot
   `service/mcp/siteimprove/full-tool-list.png` (the one most likely to reveal softening).
6. Confirm `git status` shows only `src/images` modifications and no deletions.

## Optional, not included

Three files are on disk but unreferenced from `slides.md` (2.2 MB) — `bonus/cost/mac.png`,
`service/mcp/flow/4-tool-search.png`, `service/mcp/siteimprove/chat-tool-use.png`. Say the
word and I'll delete them too; otherwise they stay.
