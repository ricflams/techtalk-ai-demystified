#!/usr/bin/env python3
"""Render the Marp slide source as a plain, GitHub-wiki-style reading page.

This bypasses the compiled Marp slideshow entirely and renders src/slides.md
through a standard Markdown pipeline, stripping only the handful of
Marp-specific directives that don't make sense outside a slideshow (YAML
frontmatter, the slideshow-only <style> blocks, the `bg` image marker).
Everything else -- headings (including the `####` speaker notes, which are
only ever hidden by the stripped <style> block), raw HTML blocks like
`.cols`, and images -- renders in natural document order.

Usage: python make_readable.py slides.md output.html
"""

import re
import sys

import markdown

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Demystified</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{style}
</style>
</head>
<body>
<article class="markdown-body">
{body}
</article>
</body>
</html>
"""

STYLE = """
body {
  margin: 0;
  background: #ffffff;
  color: #1f2328;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans",
    Helvetica, Arial, sans-serif;
  line-height: 1.6;
}
.markdown-body {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 1.5rem 6rem;
}
h1, h2, h3, h4 {
  font-weight: 600;
  line-height: 1.25;
  margin: 1.6em 0 0.6em;
}
/* Headings mark the start of a new topic (a former slide) even when there's
   no literal `---` break before them (headingDivider:3 auto-starts a new
   slide at every h3) -- give them their own separator so a paragraph never
   runs straight into the next heading. */
.markdown-body > h1:not(:first-child),
.markdown-body > h2:not(:first-child),
.markdown-body > h3:not(:first-child) {
  border-top: 1px solid #d0d7de;
  padding-top: 2rem;
  margin-top: 3rem;
}
h1 { font-size: 2em; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; padding-bottom: 0.3em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; color: #57606a; }
p { margin: 0.8em 0; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
strong { font-weight: 600; }
ul, ol { padding-left: 2em; }
li { margin: 0.25em 0; }
hr {
  border: none;
  border-top: 1px solid #d0d7de;
  margin: 3rem 0;
}
code {
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 6px;
  font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", Consolas, monospace;
  font-size: 0.85em;
}
pre {
  background: #f6f8fa;
  padding: 1em;
  border-radius: 6px;
  overflow: auto;
}
pre code { background: none; padding: 0; }
blockquote {
  border-left: 4px solid #d0d7de;
  margin: 0.8em 0;
  padding: 0 1em;
  color: #57606a;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}
th, td {
  border: 1px solid #d0d7de;
  padding: 0.5em 0.9em;
  text-align: left;
}
th { background: #f6f8fa; }
img:not(.logo) {
  /* Cap height too (roughly the 4:3-ish ratio the slideshow itself uses),
     not just width -- otherwise a tall/portrait image forced to the full
     800px column width towers over everything else on the page. Letting
     width stay auto (instead of 100%) means a capped image still shrinks
     to fit its own aspect ratio and centers via the auto margins, rather
     than stretching to fill the column. */
  max-width: 100%;
  max-height: 600px;
  width: auto;
  height: auto;
  display: block;
  margin: 1.5rem auto;
  border-radius: 4px;
}
.verdict {
  display: block;
  font-weight: 400;
  font-size: 1.25em;
  margin: 0.4em 0 1em;
}
.verdict em { color: inherit; }
.verdict.yes { color: #1a7f37; }
.verdict.no { color: #e0242e; }
.verdict.maybe { color: #9a6700; }
img.logo {
  max-width: 1.4em;
  max-height: 1.4em;
  vertical-align: -0.3em;
  display: inline;
  margin: 0 0.3em 0 0;
  box-shadow: none;
}
/* The tokenspree game slide ships its own static fallback (an image + link)
   specifically for contexts where the live iframe embed doesn't make sense
   -- this is exactly that context. */
iframe.game { display: none; }
.github-fallback { display: block; }

/* `.cols` blocks pair things that belong side by side on the slide -- an
   image next to the bullets explaining it, or two images being compared.
   Left unstyled they collapse into document order, so the image lands
   full-width above text that reads as if it were a separate section. Keep
   the pairing here, honoring the same col-N weights layout.css uses. */
.cols {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin: 1.5rem 0;
}
.cols > * { flex: 1 1 0; min-width: 0; }
.cols > .col-2 { flex: 2 1 0; }
.cols > .col-3 { flex: 3 1 0; }
.cols > .col-4 { flex: 4 1 0; }
.cols > .col-5 { flex: 5 1 0; }
.cols > .col-6 { flex: 6 1 0; }
/* Marp's markdown-it leaves a standalone `<img>` line as a raw HTML block,
   so its col-N class sits directly on the flex child. python-markdown
   instead wraps that image in a <p>, which becomes the flex child and
   carries no class -- so read the weight off the wrapped image. */
.cols > p { margin: 0; }
.cols > p:has(> .col-2) { flex: 2 1 0; }
.cols > p:has(> .col-3) { flex: 3 1 0; }
.cols > p:has(> .col-4) { flex: 4 1 0; }
.cols > p:has(> .col-5) { flex: 5 1 0; }
.cols > p:has(> .col-6) { flex: 6 1 0; }
/* Overrides the page-wide `img:not(.logo)` cap, which sizes an image to sit
   alone in the text column: inside a column an image should fill the column
   it was given. Same specificity as that rule would be a source-order tie,
   so match .logo here too and win outright. */
.cols img:not(.logo) {
  width: 100%;
  max-width: 100%;
  max-height: none;
  height: auto;
  margin: 0;
}
/* Consecutive `<img>` lines are one paragraph to python-markdown, so a row
   of images arrives as a single flex child and would stack inside it. Lay
   that paragraph out as its own row instead. */
.cols > p:has(img + img) { display: flex; gap: 1.5rem; align-items: center; }
.cols > p:has(img + img) > img:not(.logo) { flex: 1 1 0; width: auto; min-width: 0; }
/* Two-image comparisons shouldn't stretch to unequal heights. */
.cols.fit { justify-content: center; }
.cols.fit img:not(.logo) { width: auto; max-height: 420px; margin: 0 auto; }
.cols > div > :first-child { margin-top: 0; }
.cols > div > :last-child { margin-bottom: 0; }
.cols ul, .cols ol { padding-left: 1.3em; }
/* A side-by-side pair needs more room than a single column of prose, so let
   these blocks bleed a little past the 800px reading measure when the
   viewport can spare it. */
@media (min-width: 1040px) {
  .cols {
    width: calc(100% + 200px);
    margin-left: -100px;
    margin-right: -100px;
  }
}
/* Too narrow for columns: fall back to the stacked reading order. */
@media (max-width: 720px) {
  .cols, .cols > p:has(img + img) { display: block; }
  /* Back to the page's ordinary standalone-image treatment, height cap
     included, so a tall image doesn't tower over the text below it. */
  .cols img:not(.logo) {
    width: auto;
    max-width: 100%;
    max-height: 600px;
    margin: 1.5rem auto;
  }
  .cols > div + div, .cols > p + div { margin-top: 1rem; }
}
"""


def normalize_lazy_lists(text: str) -> str:
    """Insert the blank line python-markdown needs in front of a list.

    CommonMark -- GitHub, and the markdown-it parser Marp uses -- lets a list
    start on the line straight after a paragraph, so `Links:` followed
    immediately by `- [...]` is a paragraph plus a list. python-markdown
    instead swallows the items into the paragraph and renders them as one
    run-on line, so the blank line is added here rather than littering
    slides.md with blank lines that only exist to appease this script.
    """
    list_item = re.compile(r'^([-*+]|\d+[.)])\s+\S')
    fence = re.compile(r'^\s*(```|~~~)')

    out: list[str] = []
    in_fence = False
    in_list = False  # current run of non-blank lines is already a list
    for line in text.split('\n'):
        if fence.match(line):
            in_fence = not in_fence
            in_list = False
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        is_item = bool(list_item.match(line))
        # Only break out of ordinary paragraph text: a raw HTML line, an
        # indented continuation or a heading either needs no help or would be
        # damaged by the split. A list already under way must not be split
        # either -- a lone `&nbsp;` spacer line between items is a lazy
        # continuation of the item above it, not the end of the list.
        if (is_item and out and not in_list
                and out[-1].strip()
                and not out[-1].startswith((' ', '\t', '<', '>', '#'))):
            out.append('')

        if not line.strip():
            in_list = False
        elif is_item or line.startswith((' ', '\t')):
            in_list = True
        out.append(line)
    return '\n'.join(out)


def dedent_raw_html(text: str) -> str:
    """Un-indent raw HTML lines that are indented purely for readability.

    Inside a `.cols` block an `<img>` is often written indented under its
    wrapping `<div>`. markdown-it (what Marp uses) doesn't care, but
    python-markdown reads four spaces or a tab as an indented code block and
    renders the tag as literal source. Straightening the indentation here
    keeps slides.md formatted the way it reads best in the editor.
    """
    fence = re.compile(r'^\s*(```|~~~)')
    out: list[str] = []
    in_fence = False
    for line in text.split('\n'):
        if fence.match(line):
            in_fence = not in_fence
        elif not in_fence and re.match(r'^[ \t]+<', line):
            line = line.lstrip()
        out.append(line)
    return '\n'.join(out)


def transform(src: str) -> str:
    # Strip the leading YAML frontmatter block only (the very first
    # `---`-delimited block). Every other `---` in the file is a real
    # slide-break thematic break and must survive as an <hr>.
    text = re.sub(r'\A---\n.*?\n---\n', '', src, count=1, flags=re.DOTALL)

    # Strip Marp-only <style> blocks (the h4-hiding block and the game
    # slide's scoped block) -- nothing needs hiding in plain-reading mode.
    text = re.sub(r'<style\b[^>]*>.*?</style>\s*', '', text, flags=re.DOTALL | re.IGNORECASE)

    # `![bg]`, `![bg contain]`, etc. -> plain image references.
    text = re.sub(r'!\[bg[^\]]*\]', '![]', text)

    # `.cols` layouts and the game-slide fallback nest real markdown (lists,
    # links, bold text) inside raw <div> blocks. python-markdown only
    # recurses into markdown there when a block is explicitly marked
    # `markdown="1"` (unlike markdown-it, which does this by default) --
    # mark every <div> so nested content renders instead of staying literal.
    text = re.sub(r'<div(?![^>]*\bmarkdown=)', '<div markdown="1"', text)

    text = dedent_raw_html(text)

    text = normalize_lazy_lists(text)

    body = markdown.markdown(text, extensions=['extra', 'sane_lists', 'toc', 'md_in_html'])

    return PAGE_TEMPLATE.format(style=STYLE, body=body)


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} slides.md output.html', file=sys.stderr)
        sys.exit(1)

    src_path, dst_path = sys.argv[1], sys.argv[2]

    with open(src_path, 'r', encoding='utf-8') as f:
        text = f.read()

    result = transform(text)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Readable version written to {dst_path}')


if __name__ == '__main__':
    main()
