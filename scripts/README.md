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

`public/` is entirely generated and git-ignored — delete it any time.
