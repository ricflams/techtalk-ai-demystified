#!/usr/bin/env python3
"""Build the per-slide speaker-notes map used by the notes.html companion page.

Splits src/slides.md into slides using the same rules Marp itself applies
(thematic-break `---` lines, plus `headingDivider: 3` auto-splitting before
every h1/h2/h3), extracts each slide's `####`-marked note block(s), and
renders them through the same Markdown pipeline make_readable.py uses so
formatting matches the readable page exactly.

Also injects a tiny sync script into the already-built presentation.html
that broadcasts the current slide number (via BroadcastChannel) whenever
it changes, so notes.html can follow along.

Also injects a focus guard that keeps keyboard focus out of embedded
iframes, so the deck stays navigable after clicking inside one.

Note: bespoke.js's navigation updates the URL fragment via the History API
(pushState/replaceState), which does *not* fire a `hashchange` event -- so
the sync script polls `location.hash` on an interval rather than listening
for hashchange, which would silently never fire.

Usage: python make_notes.py slides.md presentation.html notes.json
"""

import json
import re
import sys

import markdown

SYNC_SCRIPT = """<script>
(function () {
  if (new URLSearchParams(location.search).has('view')) return; // skip presenter/next-slide iframes
  const bc = new BroadcastChannel('techtalk-ai-demystified:notes-sync');
  let last = null;
  const broadcast = () => {
    const hash = location.hash.slice(1) || '1';
    if (hash !== last) {
      last = hash;
      bc.postMessage(hash);
    }
  };
  setInterval(broadcast, 250);
  broadcast();
})();
</script>
"""


FOCUS_GUARD_SCRIPT = """<script>
(function () {
  // Clicking inside an embedded iframe (the tokenspree game) moves keyboard
  // focus into that iframe's document, so bespoke.js -- whose keydown handler
  // lives on the parent document -- stops seeing arrow/space/PgDn keys and the
  // deck becomes un-navigable until you click outside the frame. The embedded
  // games are click-only, so nothing is lost by bouncing focus straight back
  // out; mouse events still reach the iframe regardless of who has focus.
  // Polled rather than event-driven because focus/blur behavior on iframes is
  // inconsistent across browsers.
  setInterval(function () {
    var el = document.activeElement;
    if (el && el.tagName === 'IFRAME') {
      el.blur();
      window.focus();
    }
  }, 200);
})();
</script>
"""


def split_slides(src: str) -> list[str]:
    # Strip the leading YAML frontmatter block only, same as make_readable.py.
    text = re.sub(r'\A---\n.*?\n---\n', '', src, count=1, flags=re.DOTALL)

    # Marp extracts <style> blocks out as global CSS -- they never occupy
    # slide content, so (like make_readable.py) strip them before splitting.
    # Otherwise a <style> block sitting before a slide's first heading looks
    # like "real" preceding content and wrongly triggers a phantom slide
    # split at that heading, shifting every following slide index by one.
    text = re.sub(r'<style\b[^>]*>.*?</style>\s*', '', text, flags=re.DOTALL | re.IGNORECASE)

    # CommonMark (and Marp) thematic breaks are any line of 3+ repeated
    # `-`/`*`/`_` characters, not just a literal `---` -- e.g. `----------`
    # is a valid slide separator too and must split just like `---` does.
    thematic_break_re = re.compile(r'^ {0,3}([-*_])( *\1){2,} *$')

    slides = []
    current: list[str] = []

    def flush():
        if current:
            slides.append('\n'.join(current))

    for line in text.split('\n'):
        if thematic_break_re.match(line.rstrip('\r')):
            flush()
            current.clear()
            continue
        if re.match(r'^#{1,3}\s', line) and current:
            flush()
            current.clear()
        current.append(line)
    flush()

    return slides


def extract_notes(slide_text: str) -> str:
    lines = slide_text.split('\n')
    notes = []
    i = 0
    while i < len(lines):
        if re.match(r'^####\s*$', lines[i]):
            i += 1
            body = []
            while i < len(lines) and not re.match(r'^#{1,4}\s', lines[i]):
                body.append(lines[i])
                i += 1
            note = '\n'.join(body).strip()
            if note:
                notes.append(note)
        else:
            i += 1
    return '\n\n'.join(notes)


def count_built_slides(presentation_html: str) -> int:
    return len(re.findall(r'<section\b[^>]*\bid="\d+"', presentation_html))


def main():
    if len(sys.argv) != 4:
        print(f'Usage: {sys.argv[0]} slides.md presentation.html notes.json', file=sys.stderr)
        sys.exit(1)

    slides_path, presentation_path, notes_path = sys.argv[1:4]

    with open(slides_path, 'r', encoding='utf-8') as f:
        src = f.read()

    slides = split_slides(src)

    with open(presentation_path, 'r', encoding='utf-8') as f:
        presentation_html = f.read()

    built_count = count_built_slides(presentation_html)
    if built_count and built_count != len(slides):
        print(
            f'ERROR: parsed {len(slides)} slides from {slides_path} but '
            f'{presentation_path} contains {built_count} — the slide splitter '
            f'has drifted from Marp\'s actual behavior.',
            file=sys.stderr,
        )
        sys.exit(1)

    notes_map = {}
    for index, slide_text in enumerate(slides, start=1):
        note_md = extract_notes(slide_text)
        if note_md:
            notes_map[str(index)] = markdown.markdown(
                note_md, extensions=['extra', 'sane_lists', 'toc', 'md_in_html']
            )

    with open(notes_path, 'w', encoding='utf-8') as f:
        json.dump(notes_map, f, ensure_ascii=False)

    if '</body>' in presentation_html and 'techtalk-ai-demystified:notes-sync' not in presentation_html:
        presentation_html = presentation_html.replace(
            '</body>', SYNC_SCRIPT + FOCUS_GUARD_SCRIPT + '</body>'
        )
        with open(presentation_path, 'w', encoding='utf-8') as f:
            f.write(presentation_html)

    print(f'{len(slides)} slides parsed, {len(notes_map)} with notes -> {notes_path}')


if __name__ == '__main__':
    main()
