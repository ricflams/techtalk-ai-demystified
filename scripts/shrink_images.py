#!/usr/bin/env python3
"""Shrink src/images so the deck loads fast, without visible quality loss at HD.

The Marp canvas is 1280x720 CSS px (no `size:` directive, so Marp's default
applies), so fullscreen on an HD display the deck renders at exactly 1.5x.
A 1920x1080 source is therefore the precise point where extra pixels stop
being visible, and everything above it is pure download weight.

Three levers, in this order, all bit-exact except the resize itself:

  1. Downscale to fit a 1920x1080 box, using a single uniform scale factor
     min(1920/w, 1080/h, 1.0). Aspect ratio is never altered and images
     already inside the box are never upscaled.
  2. Format by content. A PNG with more than 65536 distinct colours is
     continuous-tone content (an illustration or photo), not the flat-colour
     UI screenshots this deck is mostly made of -- PNG's predictive row
     filters do badly on that kind of content, so it's encoded as lossless
     WebP instead (same pixels, exact alpha, smaller file). Flat-colour PNGs
     stay PNG, using an exact palette when the image genuinely has <=256
     colours. `slides.md` is updated to match any renamed file.
  3. Lossless re-encode. With --zopfli, recompress the PNG stream too (same
     pixels, smaller deflate stream) -- accurate but slow, ~20s per file.
     (WebP output is already at max effort; --zopfli affects PNGs only.)

Never grows a file: if a candidate encoding is not smaller than what's
already on disk, the original is kept untouched, even if that leaves it
above the 1920x1080 box. SVGs are left alone; JPEG/WebP sources keep their
format and are only touched when oversized.

Usage:
    python scripts/shrink_images.py [--dry-run] [--zopfli] [DIR]
"""
import io
import os
import re
import shutil
import sys
import time

from PIL import Image, ImageChops

MAX_W, MAX_H = 1920, 1080
SRC = "src/images"
SLIDES = "src/slides.md"
KEEP_FORMAT = {"jpg", "jpeg", "webp"}
# PNGs with more distinct colours than this are treated as photographic /
# illustration content and encoded as lossless WebP instead of PNG.
PHOTO_COLORS = 65536
# Marker for "re-encoding this made it bigger, so the original stayed" --
# these files are intentionally left above the box, so the box check must
# skip them.
KEPT = "kept original (re-encode larger)"


def write_file(path, data):
    """Write with retries: on Windows, antivirus/OneDrive/indexer can transiently
    hold a file handle mid-scan and raise OSError(22) on open(). A brief retry
    survives that instead of aborting a multi-hour run over a momentary lock."""
    delay = 0.5
    for attempt in range(5):
        try:
            with open(path, "wb") as fh:
                fh.write(data)
            return
        except OSError:
            if attempt == 4:
                raise
            time.sleep(delay)
            delay *= 2


def encode_png(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def encode_lossless_webp(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
    return buf.getvalue()


def is_photographic(im):
    """True when `im` has more than PHOTO_COLORS distinct colours -- i.e. it's
    continuous-tone content PNG compresses poorly, not a flat-colour screenshot."""
    return im.convert("RGB").getcolors(PHOTO_COLORS) is None


def best_png(im):
    """Smallest bit-exact PNG encoding of `im`."""
    best = encode_png(im)
    # An exact adaptive palette, but only when the image really has <=256
    # colours -- getcolors returns None above its limit, and the result is
    # verified pixel-identical before it is allowed to win.
    colors = im.getcolors(256)
    if colors:
        pal = im.convert("P", palette=Image.Palette.ADAPTIVE, colors=max(1, len(colors)))
        if not ImageChops.difference(pal.convert("RGBA"), im.convert("RGBA")).getbbox():
            cand = encode_png(pal)
            if len(cand) < len(best):
                best = cand
    return best


def load_normalized(path):
    """Open `path`, dropping an alpha channel that is uniformly opaque.

    A fully-opaque alpha channel carries no information, so removing it is
    bit-exact while saving a whole channel.
    """
    im = Image.open(path)
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        rgba = im.convert("RGBA")
        if rgba.getchannel("A").getextrema()[0] < 255:
            return rgba, True
        return rgba.convert("RGB"), False
    return im.convert("RGB"), False


def row(rel, new_rel, orig, new, note, before, after):
    return dict(rel=rel, new_rel=new_rel, orig=orig, new=new, note=note,
                before=before, after=after)


def process(path, dry_run, use_zopfli):
    rel = os.path.relpath(path, SRC).replace(os.sep, "/")
    orig_size = os.path.getsize(path)
    ext = path.rsplit(".", 1)[-1].lower()

    if ext == "svg":
        return row(rel, rel, orig_size, orig_size, "svg untouched", None, None)

    with Image.open(path) as probe:
        w0, h0 = probe.size
    scale = min(MAX_W / w0, MAX_H / h0, 1.0)
    oversized = scale < 1.0

    if ext in KEEP_FORMAT:
        if not oversized:
            return row(rel, rel, orig_size, orig_size, ext + " untouched", (w0, h0), (w0, h0))
        im, _ = load_normalized(path)
        im = im.resize((round(w0 * scale), round(h0 * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        if ext == "webp":
            im.save(buf, "WEBP", quality=92, method=6)
        else:
            im.save(buf, "JPEG", quality=92, optimize=True, progressive=True,
                    subsampling=0)
        data = buf.getvalue()
        # Same never-grow rule as the PNG path below.
        if len(data) >= orig_size:
            return row(rel, rel, orig_size, orig_size, KEPT, (w0, h0), (w0, h0))
        if not dry_run:
            write_file(path, data)
        return row(rel, rel, orig_size, len(data), ext + " resized", (w0, h0), im.size)

    # ---- PNG ----
    im, alpha = load_normalized(path)
    if oversized:
        im = im.resize((round(w0 * scale), round(h0 * scale)), Image.LANCZOS)

    if is_photographic(im):
        data = encode_lossless_webp(im)
        if len(data) >= orig_size:
            return row(rel, rel, orig_size, orig_size, KEPT, (w0, h0), (w0, h0))
        new_rel = rel.rsplit(".", 1)[0] + ".webp"
        if not dry_run:
            write_file(os.path.join(SRC, new_rel), data)
            os.remove(path)
        note = "resized" if oversized else "re-encoded"
        return row(rel, new_rel, orig_size, len(data),
                   "webp (photographic, %s)" % note + ("+a" if alpha else ""),
                   (w0, h0), im.size)

    data = best_png(im)
    note = "png resized" if oversized else "png re-encoded"

    if use_zopfli:
        import zopfli.png
        smaller = zopfli.png.optimize(data)
        # Trust nothing: only accept it if it decodes to the same pixels.
        with Image.open(io.BytesIO(smaller)) as check:
            same = check.convert("RGBA").tobytes() == im.convert("RGBA").tobytes()
        if same and len(smaller) < len(data):
            data = smaller
            note += "+zopfli"

    # Never grow a file. Flat-colour UI screenshots are often palette-encoded at
    # source; resampling interpolates between those flat colours and explodes the
    # palette, so the re-encode can land several times larger than the original.
    # When that happens the original wins outright -- fewer bytes *and* more
    # pixels -- so keep it and leave it above the box.
    if len(data) >= orig_size:
        note = KEPT if oversized else "png untouched"
        return row(rel, rel, orig_size, orig_size, note, (w0, h0), (w0, h0))

    if not dry_run:
        write_file(path, data)
    return row(rel, rel, orig_size, len(data), note + ("+a" if alpha else ""),
               (w0, h0), im.size)


def update_slides_md(renames, dry_run):
    """Rewrite src/slides.md references for every file whose extension changed.

    Paths are matched as literal `images/<rel>` tokens -- the same shape both
    `<img src="...">` and `![bg](...)` markers use -- so one substitution
    covers every reference style without needing to parse Markdown or HTML.
    """
    if not renames or not os.path.exists(SLIDES):
        return 0
    text = open(SLIDES, encoding="utf-8").read()
    n = 0
    for old_rel, new_rel in renames:
        old_ref, new_ref = "images/" + old_rel, "images/" + new_rel
        count = text.count(old_ref)
        if count:
            text = text.replace(old_ref, new_ref)
            n += count
    if n and not dry_run:
        open(SLIDES, "w", encoding="utf-8", newline="\n").write(text)
    return n


def main():
    args = list(sys.argv[1:])
    dry_run = "--dry-run" in args
    use_zopfli = "--zopfli" in args
    rest = [a for a in args if not a.startswith("--")]
    root = rest[0] if rest else SRC

    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(root) for f in fs)
    rows = []
    failures = []
    for i, path in enumerate(files, 1):
        rows.append(process(path, dry_run, use_zopfli))
        if i % 25 == 0 or i == len(files):
            print("  ...%d/%d" % (i, len(files)), file=sys.stderr, flush=True)

    # --- invariants: no upscale, no aspect-ratio drift, nothing over the box ---
    for r in rows:
        if r["before"] is None or r["after"] is None:
            continue
        (bw, bh), (aw, ah) = r["before"], r["after"]
        if aw > bw or ah > bh:
            failures.append("%s: upscaled %dx%d -> %dx%d" % (r["new_rel"], bw, bh, aw, ah))
        if (aw > MAX_W or ah > MAX_H) and r["note"] != KEPT:
            failures.append("%s: exceeds box at %dx%d" % (r["new_rel"], aw, ah))
        drift = abs(aw / ah - bw / bh) / (bw / bh)
        if drift > 0.005:
            failures.append("%s: aspect drift %.3f%%" % (r["new_rel"], drift * 100))

    renames = [(r["rel"], r["new_rel"]) for r in rows if r["rel"] != r["new_rel"]]
    refs_updated = update_slides_md(renames, dry_run) if root == SRC else 0

    rows.sort(key=lambda r: r["orig"] - r["new"], reverse=True)
    before_total = sum(r["orig"] for r in rows)
    after_total = sum(r["new"] for r in rows)

    print("\n--- 25 biggest reductions ---")
    print("%-52s %8s %8s %5s  %-28s %s" % ("file", "before", "after", "pct", "action", "dims"))
    for r in rows[:25]:
        b, a = r["before"], r["after"]
        dims = "%dx%d -> %dx%d" % (b + a) if b and a and b != a else ""
        name = r["new_rel"] if r["rel"] != r["new_rel"] else r["rel"]
        print("%-52s %7.0fK %7.0fK %4.0f%%  %-28s %s"
              % (name, r["orig"] / 1024, r["new"] / 1024, 100 * r["new"] / r["orig"],
                 r["note"], dims))

    touched = sum(1 for r in rows if r["orig"] != r["new"])
    print("\n%d of %d files changed" % (touched, len(rows)))
    print("TOTAL %.1f MB -> %.1f MB  (%.0f%% of original, saves %.1f MB)"
          % (before_total / 1e6, after_total / 1e6,
             100 * after_total / before_total, (before_total - after_total) / 1e6))
    if dry_run:
        print("(dry run -- nothing written)")

    if failures:
        print("\nINVARIANT FAILURES:", file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        return 1

    converted = [r for r in rows if "webp (photographic" in r["note"]]
    if converted:
        saved = sum(r["orig"] - r["new"] for r in converted)
        print("\n%d PNGs converted to lossless WebP (photographic content), saving %.1f MB:"
              % (len(converted), saved / 1e6))
        for r in sorted(converted, key=lambda r: -(r["orig"] - r["new"]))[:5]:
            print("  %7.0fK -> %6.0fK  %s" % (r["orig"] / 1024, r["new"] / 1024, r["new_rel"]))
        if root == SRC:
            print("%s: updated %d reference(s)%s"
                  % (SLIDES, refs_updated, " (dry run, not written)" if dry_run else ""))

    kept = [r for r in rows if r["note"] == KEPT]
    if kept:
        print("\n%d files deliberately left above %dx%d: re-encoding cost more bytes"
              % (len(kept), MAX_W, MAX_H))
        print("than the original, so the original wins on both size and resolution.")
        print("Largest:")
        for r in sorted(kept, key=lambda r: -r["orig"])[:5]:
            print("  %7.0fK %s (%dx%d)" % (r["orig"] / 1024, r["rel"], r["before"][0], r["before"][1]))
    print("\ninvariants OK: no upscales, no aspect-ratio drift, nothing grew")
    return 0


if __name__ == "__main__":
    sys.exit(main())
