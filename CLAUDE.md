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

To preview the **readable** page instead, run `scripts\build-readable.ps1` (or `scripts/build-readable.sh`): it renders `public/index.html` and opens it. Add `-Watch` / `--watch` to rebuild on every save. It needs only `pip install markdown` — not the Marp CLI — and takes about 0.3s per rebuild.

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

Slide layout is driven entirely by which heading a slide carries (h1 → act, h2 → chapter, h3 → section), via `:has()` rules in `marp-theme.css` — there are no `<!-- _class: -->` directives anywhere in `slides.md`.

### Writing slide body text

`.marprc.yml` sets `breaks: false`, so Marp follows standard CommonMark: **a single newline is a space, not a line break.** This matches python-markdown, which builds the readable page and the speaker notes, so both outputs render the same source identically.

- **Separate blocks** — leave a blank line. Paragraphs and list items get airy spacing from the theme (`section:has(h3) > :is(p,ul,ol) + …` and `li + li`), so no manual spacers are needed.
- **A hard break inside one block** (a stanza, a paired definition) — end the line with `<br>`.
- Body blocks on h3 slides share one centered 40em column, so paragraphs and lists line up on a common left edge automatically. Gluing lines together with `<br>` purely to make them share an edge is no longer necessary.

### Promoting a slide into the contents

The readable page's contents list (built by `scripts/make_readable.py`) shows h1 chapters and their h2 sections. To pull an individual h3 slide in at section level, tag it in `slides.md`:

```markdown
### #7/11: Skills
<!-- toc-entry Skills -->
```

The heading stays an h3 in the slideshow; only the contents list changes. The text after `toc-entry` is optional and overrides the label, so a heading that reads "#7/11: Skills" on the slide can appear as just "Skills" in the contents. A bare `<!-- toc-entry -->` promotes the heading under its own name.

The marker deliberately avoids `key: value` shape so Marp can never mistake it for one of its own directives. Put it on the line directly after the heading (directly before also works, but then Marp files the stray comment as a presenter note against the *previous* slide). Marp turns any standalone comment into a `bespoke-marp-note`, which is invisible on the slide and unused by this deck — the speaker notes here come from `####` markers via `make_notes.py`.

### Section anchors on the readable page

Every h1/h2/h3 on `public/index.html` gets an HTML `id` automatically — `make_readable.py`'s `toc` extension slugifies the title text (`### The direction for "sadness"` → `index.html#the-direction-for-sadness`). That slug moves whenever the title is reworded, breaking any link pointing at it, so landmark headings are pinned to a stable id with a marker:

```markdown
## Training
<!-- anchor llm-training -->
```

`apply_anchor_markers` in `make_readable.py` turns that into `id="llm-training"` (via python-markdown `attr_list` syntax) and drops the marker line. The contents list links to whatever id a heading ends up with, so pinned headings are linked by their stable id too. Same comment shape and placement rules as `<!-- toc-entry -->` (bare word, not `key: value`; on the line right after the heading, with blank lines or a `toc-entry` comment allowed in between). It only affects the readable page — the Marp slideshow navigates by slide number, not heading id.

Convention in use — the slug mirrors the deck structure, slugified from the title with a leading `The` dropped (a couple of long chapter titles get a hand-picked short form instead):

- **h1 chapter** → `llm`, `ai-agents`, `ai-service`, `context-economy`, `how-to` (`# 3 x How to ...`), `demystifications` (`# A Quick Round of Demystifications`), `bonus`, …
- **h2 section** → `<chapter>-<section>`: `llm-tokens`, `llm-training`, `ai-service-mcp-servers`, `bonus-rag`, `bonus-a-fancy-autocomplete`, …

Pin a fragile-but-linkable h3 the same way (`<chapter>-<slug>`); leave the long tail to auto-slug. Pinning also heads off the order-dependent `-1` suffix python-markdown appends when two headings would slugify to the same id.

`add_headerlinks` then hangs a GitHub-style chain-link glyph (`.headerlink`) in every h1/h2/h3's left gutter — hidden until the heading is hovered/focused on desktop, shown inline and always tappable below 700px.
