# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A [Marp](https://marp.app/) presentation on LLM fundamentals ("AI Demystified"), authored in Markdown and deployed to GitHub Pages.

## Build

There is no package.json or Makefile. The slide deck is compiled with the Marp CLI:

```bash
marp src/slides.md --html --theme src/marp-theme.css --output public/presentation.html
cp -r src/images public/images
cp src/layout.css public/layout.css
pip install markdown
python3 scripts/make_readable.py src/slides.md public/index.html
python3 scripts/make_notes.py src/slides.md public/presentation.html public/notes.json
cp src/notes.html public/notes.html
```

Note: `marp-theme.css` pulls in `layout.css` via `@import`, which Marp CLI leaves unresolved in the output HTML (it does not inline `@import`s) — `layout.css` must be copied next to the built HTML so the browser can fetch it at runtime.

`public/index.html` (the readable, non-slideshow version) is generated independently from `src/slides.md` directly — it does **not** post-process `public/presentation.html`. `scripts/make_readable.py` strips the Marp-only bits (YAML frontmatter, the two `<style>` blocks used to hide slide-only content, the `![bg ...]` background-image marker) and renders the rest through the `markdown` pip package with a small self-contained GitHub-wiki-style stylesheet, so it needs its own dependency (`pip install markdown`) and never touches `marp-theme.css`/`layout.css`.

In CI, this runs inside the `marpteam/marp-cli:latest` Docker container. Pushing to `main` triggers `.github/workflows/marp.yaml`, which builds both outputs and deploys to GitHub Pages automatically.

For local preview, the [VS Code Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) renders slides in the editor — `.vscode/settings.json` already points it at the custom theme.

### Speaker notes

Each slide can carry a presenter-only note: a bare `####` marker followed by prose, hidden from the compiled slideshow by a global CSS rule at the top of `src/slides.md` (`h4, h4 ~ * { display: none; }`). These notes render as ordinary content on the readable page (`public/index.html`) since that page is built independently from the same markdown.

For remote presenting (screen-sharing `presentation.html` in a call), `scripts/make_notes.py` builds `public/notes.json` — a `{slide index: rendered note HTML}` map — and injects a small script into `presentation.html` that broadcasts the current slide number (via `BroadcastChannel`) whenever its URL hash changes. `notes.html` (copied from `src/notes.html`) listens on that channel and displays the matching note live. Open `presentation.html` (shared/fullscreen) and `notes.html` (kept private, on your own screen) as two tabs of the same deployed site — they sync automatically as you navigate slides.

## Architecture

| Path | Purpose |
|---|---|
| `src/slides.md` | All slide content (single source of truth) |
| `src/marp-theme.css` | Custom dark theme (GitHub Copilot palette: `#0d1117` background, `#58a6ff`/`#bc8cff` accents) |
| `src/layout.css` | Shared layout helpers (imported by both `marp-theme.css` and `.crossnote/style.less`) |
| `src/notes.html` | Speaker-notes companion page, synced live to `presentation.html` via `BroadcastChannel` |
| `scripts/make_readable.py` | Post-processes Marp HTML into a continuous-scroll readable page |
| `scripts/make_notes.py` | Builds `public/notes.json` and injects the sync script into `presentation.html` |
| `.github/workflows/marp.yaml` | Build + GitHub Pages deploy |
| `public/presentation.html` | Interactive slideshow — build artifact (generated, not committed) |
| `public/index.html` | Continuous-scroll readable version — build artifact (generated, not committed) |
| `public/notes.html` | Speaker-notes companion page — build artifact (generated, not committed) |
| `public/notes.json` | Per-slide rendered notes map — build artifact (generated, not committed) |

### Marp slide structure

Slides are separated by `---`. The theme is declared in the frontmatter:

```markdown
---
marp: true
theme: custom-theme
---
```

Custom slide layout classes defined in `marp-theme.css`: `lead`, `chapter`, `invert`, `highlight`. Apply them with `<!-- _class: chapter -->` directives inside a slide.
