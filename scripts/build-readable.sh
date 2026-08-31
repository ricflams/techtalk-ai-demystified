#!/usr/bin/env bash
# Build the readable (non-slideshow) page locally and open it in a browser.
#
# Renders src/slides.md to public/index.html via make_readable.py and syncs the
# images it references. This is the same output GitHub Pages publishes as the
# site's front page -- it does NOT build the slideshow (that needs the Marp
# CLI; see CLAUDE.md). The page is plain static HTML with relative image
# paths, so it opens straight from disk -- no local web server needed.
#
# Usage:
#   scripts/build-readable.sh            build once and open it
#   scripts/build-readable.sh --watch    rebuild on every save
#   scripts/build-readable.sh --no-open  build only
set -euo pipefail
cd "$(dirname "$0")/.."

watch=0
open_after=1
for arg in "$@"; do
  case "$arg" in
    --watch)   watch=1 ;;
    --no-open) open_after=0 ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

slides=src/slides.md
script=scripts/make_readable.py
output=public/index.html

# python3 on Linux/macOS, python on Windows (git-bash) where python3 is a
# Microsoft Store stub that isn't a real interpreter.
py=python3
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 || py=python

build() {
  mkdir -p public
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete src/images/ public/images/
  else
    # Copy the *contents* into the directory. `rm -rf` then `cp -r src/images
    # public/images` looks equivalent but isn't: if the remove is refused (a
    # browser or server on Windows can hold a handle open), the copy nests a
    # second images/ inside the old one instead of replacing it.
    mkdir -p public/images
    cp -r src/images/. public/images/
  fi
  if ! "$py" "$script" "$slides" "$output"; then
    echo "make_readable.py failed. If it can't import 'markdown', run: pip install markdown" >&2
    return 1
  fi
}

open_page() {
  if command -v xdg-open >/dev/null 2>&1;   then xdg-open "$output"
  elif command -v open >/dev/null 2>&1;     then open "$output"
  elif command -v start >/dev/null 2>&1;    then start "$output"
  else echo "Open $output in your browser."
  fi
}

build
echo "Built $output"
[ "$open_after" -eq 1 ] && open_page

[ "$watch" -eq 0 ] && exit 0

echo "Watching $slides -- press Ctrl-C to stop. Refresh the browser (F5) after each rebuild."

# Polled rather than inotify: keeps this dependency-free and works the same on
# macOS and in git-bash on Windows. `stat -c` is GNU, `stat -f` is BSD/macOS.
if stat -c %Y "$slides" >/dev/null 2>&1; then
  stamp() { stat -c %Y "$slides" "$script" | tr '\n' ','; }
else
  stamp() { stat -f %m "$slides" "$script" | tr '\n' ','; }
fi
last=$(stamp)
while true; do
  sleep 0.5
  now=$(stamp)
  [ "$now" = "$last" ] && continue
  last=$now
  if build; then
    echo "[$(date +%H:%M:%S)] rebuilt"
  fi
done
