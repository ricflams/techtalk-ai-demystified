#!/usr/bin/env bash
# Rebuild the readable (non-slideshow) page for local preview.
# Usage: scripts/build-readable.sh
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf public/images
cp -r src/images public/images
python scripts/make_readable.py src/slides.md public/index.html

echo "Open public/index.html directly in a browser to preview."
