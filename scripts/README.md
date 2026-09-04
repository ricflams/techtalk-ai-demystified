# scripts/

How to build and preview this deck locally. Everything renders from the single
source file, `src/slides.md`.

There are two outputs, built by two independent pipelines:

| Output | What it is | Needs |
|---|---|---|
| `public/index.html` | the **readable** page — one continuous scroll, speaker notes visible | `pip install markdown` |
| `public/presentation.html` | the **slideshow** — the thing you present from | the Marp CLI |

You almost always want the readable page. It's the fast one, and it's what
GitHub Pages serves as the site's front page.

---

## Build the readable page

```powershell
scripts\build-readable.ps1              # build, then open it in your browser
scripts\build-readable.ps1 -Watch       # rebuild on every save
scripts\build-readable.ps1 -NoOpen      # build only
```

```bash
scripts/build-readable.sh [--watch] [--no-open]
```

About 0.3s per rebuild. The page is static HTML with relative image paths, so
it opens straight from disk — no local web server needed. With `-Watch`, press
F5 in the browser after each save.

One-time setup: `pip install markdown`.

This is the same script CI runs (`.github/workflows/marp.yaml` calls
`scripts/build-readable.sh --no-open`), so local and published output can't
drift apart.

> If you edit `build-readable.sh`, keep its executable bit — `git update-index
> --chmod=+x scripts/build-readable.sh`. Without it the CI step fails with
> "Permission denied".

## Build the slideshow

Needs the Marp CLI (`npm i -g @marp-team/marp-cli`); CI uses the
`marpteam/marp-cli:latest` Docker image instead.

```bash
marp src/slides.md --html --theme src/marp-theme.css --output public/presentation.html
cp src/layout.css public/layout.css
```

`layout.css` must sit next to the built HTML: `marp-theme.css` pulls it in with
`@import`, which the Marp CLI leaves unresolved rather than inlining.

For editing, the [VS Code Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
previews slides live in the editor — `.vscode/settings.json` already points it
at the custom theme.

## Build the speaker notes companion

```bash
python scripts/make_notes.py src/slides.md public/presentation.html public/notes.json
cp src/notes.html public/notes.html
```

Run this **after** the slideshow build — it reads `presentation.html` and
injects a sync script into it.

It also guards against drift: it fails loudly if the number of slides it parses
from the markdown doesn't match the number Marp actually produced.

## Build everything, the way CI does

```bash
marp src/slides.md --html --theme src/marp-theme.css --output public/presentation.html
cp src/layout.css public/layout.css
scripts/build-readable.sh --no-open
python scripts/make_notes.py src/slides.md public/presentation.html public/notes.json
cp src/notes.html public/notes.html
cp -r demo/tokenspree public/tokenspree
```

Pushing to `main` does all of this and deploys to GitHub Pages automatically.

## Shrink the images

`src/images` is capped at 1920x1080. Marp puts every slide in one HTML file, so the
browser fetches all the images up front — oversized ones are pure download weight. The
1280x720 canvas renders at 1.5x fullscreen on an HD display, so past 1920x1080 the extra
pixels can't be seen.

```bash
python scripts/shrink_images.py --dry-run   # report only, writes nothing
python scripts/shrink_images.py             # rewrite src/images in place
python scripts/shrink_images.py --zopfli    # + lossless deflate pass, ~20s/file
```

Run it after adding new screenshots or illustrations. It downscales with one uniform scale
factor, so aspect ratios never change and anything already inside the box is left alone; it
aborts if that ever fails to hold. One-time setup: `pip install pillow`.

It also picks a format by content: a PNG with more than 65536 distinct colours (an
illustration or photo, not a flat-colour screenshot) is re-encoded as lossless WebP instead
— same pixels, exact alpha, smaller file — and it renames the file and updates the matching
`images/...` references in `src/slides.md` for you. A ShareX-style capture is always
flat-colour, so new screenshots always stay PNG; the extension you type while authoring a
slide never has to guess ahead of a later optimization pass.

Originals live in git history — `git restore src/images` undoes a run (note: a full
`restore` reverts *every* prior pass, not just the last one, since nothing is committed
between runs — commit after a pass you want to keep).

## Present

```powershell
scripts\present.ps1
```

Opens two browser windows against the deployed site: `presentation.html` to
share or fullscreen, and `notes.html` to keep on your own screen. They sync
over `BroadcastChannel` as you move through the deck.

---

## What each file does

| File | |
|---|---|
| `build-readable.ps1` / `.sh` | build + open the readable page; `-Watch` to rebuild on save |
| `make_readable.py` | renders `slides.md` to the readable page (called by the above) |
| `make_notes.py` | builds `notes.json` and injects the slide-sync script into `presentation.html` |
| `present.ps1` | opens the deployed slideshow + notes windows for presenting |
| `shrink_images.py` | caps `src/images` at 1920x1080; losslessly re-encodes PNGs, converting photographic ones to WebP |

`public/` is entirely generated and git-ignored — delete it any time.
