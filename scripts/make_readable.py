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
/* GitHub-style section anchor: a chain-link glyph in the left gutter, hidden
   until the heading (or the link itself) is hovered or keyboard-focused.
   Absolutely positioned with no `top`, so it sits on the heading's first
   line; `left` pulls it into the column's left padding. */
.markdown-body :is(h1, h2, h3) { position: relative; }
.headerlink {
  position: absolute;
  left: -1.15em;
  opacity: 0;
  color: #8c959f;
  transition: opacity 0.1s;
}
.headerlink svg { display: block; width: 0.8em; height: 0.8em; fill: currentColor; }
.headerlink:hover { color: #0969da; }
.markdown-body :is(h1, h2, h3):hover > .headerlink,
.headerlink:focus-visible { opacity: 1; }
/* Narrow screens: no left gutter to hang the glyph in, and no hover to reveal
   it -- drop it inline after the heading, faint but always tappable. */
@media (max-width: 699px) {
  .headerlink {
    position: static;
    opacity: 1;
    margin-left: 0.4em;
    color: #d0d7de;
    vertical-align: middle;
  }
  .headerlink svg { display: inline-block; }
}
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
  /* A dark hairline so an image reads as an image and not as page content --
     screenshots on a white background otherwise dissolve into the page. Dark
     rather than the usual #d0d7de chrome grey because the deck mixes light and
     dark images: on the ~60 dark ones the border simply disappears into the
     image, while a light border would be the one doing nothing on the ~127
     light ones, which are the case that actually needs bounding. */
  border: 1px solid #57606a;
  border-radius: 6px;
}
/* Contents, sitting just under the title slide. Chapters (h1) go on their own
   lines with no bullets; the sections (h2) inside each run together on one
   indented line, so the whole deck fits in one glance. Every entry is a plain
   link -- the indentation alone carries the hierarchy. */
.toc {
  margin: 0.5rem 0 1rem;
  line-height: 1.8;
}
/* Quieter than a page h2 -- it labels the block without competing with the
   deck title just above it. */
.toc-title {
  font-size: 1.15em;
  font-weight: 600;
  margin: 0 0 0.5em;
  padding: 0;
  border: none;
}
/* padding-left on an inline span indents the line it starts, which is what a
   run of sections needs -- and if it wraps, the continuation lines sit flush,
   keeping a long run visually subordinate to its chapter. */
.toc-sections {
  padding-left: 1.6rem;
  font-size: 0.95em;
}
.toc-sep {
  color: #8c959f;
  padding: 0 0.5em;
  font-size: 0.8em;
  /* The separator is furniture, not content -- keep it out of a copied
     selection and out of the accessibility tree. */
  user-select: none;
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
.cols > .col-7 { flex: 7 1 0; }
.cols > .col-8 { flex: 8 1 0; }
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
.cols > p:has(> .col-7) { flex: 7 1 0; }
.cols > p:has(> .col-8) { flex: 8 1 0; }
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


def build_toc(body: str) -> str:
    """Build the contents block from the rendered h1/h2 headings.

    Each h1 (a chapter) gets its own line; the h2s inside it run together on
    one indented line beneath, separated by bullets -- they're signposts for
    what a chapter covers, not a list you read top to bottom.

    Kept deliberately compact -- plain <br>-separated lines rather than block
    elements -- so the whole deck fits in one glance.

    The first h1 is the deck's own title slide, which the contents sits
    directly under, so it is skipped.

    An h3 can be pulled into the contents at section level by tagging it in
    slides.md with a `<!-- toc-entry -->` comment on the line right after (or
    before) the heading. `<!-- toc-entry Skills -->` also overrides the label,
    so a heading that reads "#7/11: Skills" on the slide can appear as just
    "Skills" here. Deliberately not `key: value` shaped, so it can never be
    taken for one of Marp's own directives.

    Contents links point at whatever `id` each heading ended up with, so a
    heading pinned with `<!-- anchor -->` (see `apply_anchor_markers`) is
    linked by that stable id automatically.
    """
    def text_of(markup: str) -> str:
        plain = re.sub(r'<br\s*/?>', ' ', markup)
        plain = re.sub(r'<[^>]+>', '', plain)
        return re.sub(r'\s+', ' ', plain).strip()

    token = re.compile(
        r'<!--\s*toc-entry\b\s*(?P<label>.*?)\s*-->'
        r'|<h(?P<lvl>[123]) id="(?P<anchor>[^"]+)">(?P<markup>.*?)</h(?P=lvl)>',
        re.DOTALL)
    tokens = list(token.finditer(body))

    # Bind each marker to exactly one heading, preferring the heading directly
    # above it (the documented placement). Without claiming it, a marker
    # written between two headings would tag both of them.
    is_heading = [t.group('lvl') is not None for t in tokens]
    marker_for: dict[int, re.Match] = {}
    for i, m in enumerate(tokens):
        if is_heading[i]:
            continue
        if i and is_heading[i - 1] and (i - 1) not in marker_for:
            marker_for[i - 1] = m
        elif i + 1 < len(tokens) and is_heading[i + 1]:
            marker_for[i + 1] = m

    sections: list[tuple[str, str, list[tuple[str, str]]]] = []
    for i, m in enumerate(tokens):
        if not is_heading[i]:
            continue
        marker = marker_for.get(i)
        title = (marker.group('label') if marker and marker.group('label')
                 else text_of(m.group('markup')))
        level, anchor = int(m.group('lvl')), m.group('anchor')

        if level == 1:
            sections.append((anchor, title, []))
        elif (level == 2 or marker) and sections:
            sections[-1][2].append((anchor, title))

    if len(sections) < 2:
        return ''

    lines = []
    for anchor, title, subs in sections[1:]:
        lines.append(f'<a href="#{anchor}">{title}</a>')
        if subs:
            links = [f'<a href="#{a}">{t}</a>' for a, t in subs]
            lines.append('<span class="toc-sections">'
                         + '<span class="toc-sep">&bull;</span>'.join(links)
                         + '</span>')
    return ('<nav class="toc">\n'
            '<h2 class="toc-title">Jump straight to&hellip;</h2>\n'
            + '<br>\n'.join(lines)
            + '\n</nav>')


def insert_toc(body: str) -> str:
    """Place the contents just after the title slide.

    The first `<hr>` is the slide break closing the title slide, so the
    contents lands between the title and the first chapter.
    """
    toc = build_toc(body)
    if not toc:
        return body
    first_break = re.search(r'<hr\s*/?>', body)
    if not first_break:
        return body
    return body[:first_break.end()] + '\n' + toc + body[first_break.end():]


# GitHub's own anchor glyph (Octicon "link", 16px grid).
_HEADERLINK_ICON = (
    '<svg viewBox="0 0 16 16" aria-hidden="true">'
    '<path d="M7.775 3.275a.75.75 0 0 0 1.06 1.06l1.25-1.25a2 2 0 1 1 2.83 '
    '2.83l-2.5 2.5a2 2 0 0 1-2.83 0 .75.75 0 0 0-1.06 1.06 3.5 3.5 0 0 0 '
    '4.95 0l2.5-2.5a3.5 3.5 0 0 0-4.95-4.95l-1.25 1.25Zm-4.69 9.64a2 2 0 0 '
    '1 0-2.83l2.5-2.5a2 2 0 0 1 2.83 0 .75.75 0 0 0 1.06-1.06 3.5 3.5 0 0 '
    '0-4.95 0l-2.5 2.5a3.5 3.5 0 0 0 4.95 4.95l1.25-1.25a.75.75 0 0 0-1.06'
    '-1.06l-1.25 1.25a2 2 0 0 1-2.83 0Z"></path></svg>'
)


def add_headerlinks(body: str) -> str:
    """Prepend a GitHub-style `#`-link to every h1/h2/h3 that carries an id.

    Runs after `insert_toc`, so the contents block (which parses bare
    `<hN id="...">`) never sees this markup, and the injected `<nav>`'s own
    `<h2 class="toc-title">` -- which has no id -- is skipped. Styling lives
    in STYLE under `.headerlink`.
    """
    def decorate(m: re.Match) -> str:
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        id_match = re.search(r'\bid="([^"]+)"', attrs)
        if not id_match:
            return m.group(0)
        anchor = id_match.group(1)
        link = (f'<a class="headerlink" href="#{anchor}" '
                f'aria-label="Permalink to this section">{_HEADERLINK_ICON}</a>')
        return f'<h{level}{attrs}>{link}{inner}</h{level}>'

    return re.sub(r'<h([123])([^>]*)>(.*?)</h\1>', decorate, body, flags=re.DOTALL)


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


def apply_anchor_markers(text: str) -> str:
    """Honor `<!-- anchor stable-id -->` markers: pin a heading's HTML id.

    Every h1/h2/h3 already gets an `id` automatically -- the `toc` extension
    slugifies the title text. That slug changes whenever the title is
    reworded, silently breaking any link pointing at it. Putting

        ### Post-training reshapes the model
        <!-- anchor llm-post-training -->

    on the line directly after a heading fixes that heading's id to
    `llm-post-training` for good, no matter how the title later changes.
    Untagged headings keep their auto-slug -- tag only the ones worth linking
    to (chapters, sections, the odd memorable slide).

    Mirrors the `<!-- toc-entry -->` convention: a bare-word HTML comment, not
    `key: value` shaped, so Marp can't mistake it for one of its own
    directives, and invisible on the compiled slide. Blank lines and other
    standalone comments (e.g. a `toc-entry` on its own line) may sit between
    the heading and the marker. Placement *before* the heading also works but
    is discouraged -- Marp files a comment that precedes a slide's heading as
    a note against the previous slide.

    Implemented by appending python-markdown's `attr_list` syntax
    (`{: #id }`) to the heading line, which both `attr_list` and `toc` then
    honor; the marker line itself is dropped.
    """
    lines = text.split('\n')
    is_heading = re.compile(r'^#{1,3}\s+\S')
    is_comment = re.compile(r'^\s*<!--.*-->\s*$')
    anchor = re.compile(r'^\s*<!--\s*anchor\s+([A-Za-z0-9][\w-]*)\s*-->\s*$')

    def nearest_heading(start: int, step: int) -> int | None:
        j = start + step
        while 0 <= j < len(lines):
            if not lines[j].strip() or is_comment.match(lines[j]):
                j += step
                continue
            return j if is_heading.match(lines[j]) else None
        return None

    claimed: set[int] = set()
    drop: set[int] = set()
    for i, line in enumerate(lines):
        m = anchor.match(line)
        if not m:
            continue
        for step in (-1, 1):  # heading above the marker first (the norm)
            j = nearest_heading(i, step)
            if j is not None and j not in claimed:
                lines[j] = lines[j].rstrip() + f' {{: #{m.group(1)} }}'
                claimed.add(j)
                drop.add(i)
                break

    return '\n'.join(l for i, l in enumerate(lines) if i not in drop)


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

    # `<!-- anchor stable-id -->` markers -> pinned heading ids (the rest
    # auto-slug from their title via the `toc` extension).
    text = apply_anchor_markers(text)

    # `.cols` layouts and the game-slide fallback nest real markdown (lists,
    # links, bold text) inside raw <div> blocks. python-markdown only
    # recurses into markdown there when a block is explicitly marked
    # `markdown="1"` (unlike markdown-it, which does this by default) --
    # mark every <div> so nested content renders instead of staying literal.
    text = re.sub(r'<div(?![^>]*\bmarkdown=)', '<div markdown="1"', text)

    text = dedent_raw_html(text)

    text = normalize_lazy_lists(text)

    body = markdown.markdown(text, extensions=['extra', 'sane_lists', 'toc', 'md_in_html'])

    body = insert_toc(body)

    body = add_headerlinks(body)

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
