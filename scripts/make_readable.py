#!/usr/bin/env python3
"""Transform a Marp presentation HTML into a continuous-scroll readable page.

Usage: python make_readable.py input.html output.html
"""

import re
import sys

OVERRIDE_CSS = """
/* ── Readable-mode overrides ──────────────────────────────────── */
html, body {
  overflow: auto !important;
  height: auto !important;
}
#p, .bespoke-marp-parent {
  position: static !important;
  overflow: visible !important;
  height: auto !important;
}
.bespoke-marp {
  position: static !important;
  height: auto !important;
}
section {
  position: static !important;
  display: block !important;
  width: 100% !important;
  max-width: 1500px !important;
  height: auto !important;
  min-height: unset !important;
  margin: 0 auto 5rem auto !important;
  transform: none !important;
  overflow: visible !important;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
/* Unhide speaker notes (h4 and everything that follows it in a slide) */
h4, h4 ~ * {
  display: revert !important;
}
h4 {
  opacity: 0.55;
  font-size: 0.8em !important;
  text-transform: none !important;
  letter-spacing: normal !important;
  border-top: 1px solid rgba(255,255,255,0.12);
  padding-top: 0.8rem !important;
  margin-top: 1.5rem !important;
  color: #8b949e !important;
}
/* ──────────────────────────────────────────────────────────────── */
"""


def transform(src: str) -> str:
    # Remove all <script> blocks (bespoke.js navigation + keyboard handlers)
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.DOTALL | re.IGNORECASE)

    # Inject override CSS before the first </style>
    html = html.replace('</style>', OVERRIDE_CSS + '</style>', 1)

    return html


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} input.html output.html', file=sys.stderr)
        sys.exit(1)

    src_path, dst_path = sys.argv[1], sys.argv[2]

    with open(src_path, 'r', encoding='utf-8') as f:
        html = f.read()

    result = transform(html)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Readable version written to {dst_path}')


if __name__ == '__main__':
    main()
