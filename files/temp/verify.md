# Verify the deck

Sanity checks for `src/slides.md` and the build, distilled from the passes that actually caught
bugs. Run what the size of your edit warrants: **Tier 1** after any text edit (seconds, no build),
**Tier 2** before pushing, **Tier 3** occasionally.

Everything here is self-contained — paste the blocks as-is. Run from the **repo root in git-bash**
(not PowerShell — see *Environment gotchas* at the bottom).

---

## Tier 1 — text checks, no build

### 1. Text that markdown eats as an HTML tag

The highest-value check here. `<mandatory>` and `<let me think about that>` are valid tag *syntax*,
so Marp passes them through and the browser drops them as unknown elements — the words vanish from
the slide with no warning anywhere.

```bash
python - <<'PY'
import re
KNOWN = set('a b blockquote br code col div em h1 h2 h3 h4 h5 h6 hr iframe img li ol p pre section '
            'small span strong style sub sup table tbody td th thead tr u ul video source figure'.split())
s = open('src/slides.md', encoding='utf-8').read()
s = re.sub(r'`[^`]*`|<style.*?</style>|<!--.*?-->', '', s, flags=re.DOTALL)
hits = sorted({m.group(0) for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', s)
               if m.group(2).lower() not in KNOWN})
print(hits or 'clean')
PY
```

**Fix:** escape as `&lt;word&gt;`, or wrap in backticks if it's meant as code.

### 2. YouTube links

Links use `- [exact title](https://youtu.be/ID) - Channel (m:ss)`. Two bugs have appeared here:
the host `www.youtu.be` (which does not resolve — youtu.be has no `www`), and links missing the
channel/duration annotation.

```bash
echo "malformed host : $(grep -c 'www\.youtu\.be' src/slides.md)   (want 0)"
echo "link lines     : $(grep -c '^- \[.*youtu\.be' src/slides.md)"
echo "--- lines not matching the annotated format ---"
grep -n '^- \[.*youtu\.be' src/slides.md \
  | grep -vE ':- \[.*\]\(https://youtu\.be/[A-Za-z0-9_-]+\) - .+ \([0-9]+:[0-9]{2}(:[0-9]{2})?\)$' \
  || echo "all conform"
```

Channel and playlist links (`youtube.com/@name`, `youtube.com/playlist?list=`) are deliberately
*not* annotated — they have no single duration.

### 3. Link syntax

```bash
python - <<'PY'
import re
bad = []
for n, l in enumerate(open('src/slides.md', encoding='utf-8'), 1):
    if re.search(r'!?\[[^\]]*\]\(\s*\)', l):        bad.append((n, 'empty link target', l))
    if re.search(r'\][ \t]+\(https?://', l):        bad.append((n, 'space between ] and (', l))
    for m in re.finditer(r'!?\[[^\]]*\]\(([^)\s]*)\s+([^)]*)\)', l):
        if not m.group(2).startswith('"'):          bad.append((n, 'space inside link target', l))
for n, why, l in bad:
    print(f'{n}: {why}: {l.strip()[:90]}')
print('clean' if not bad else f'{len(bad)} issue(s)')
PY
```

### 4. Emphasis, backticks, fences

Catches things like `the* core meaning*`, which renders the asterisks literally.

```bash
python - <<'PY'
import re
lines = open('src/slides.md', encoding='utf-8').read().split('\n')
fence = style = 0
for n, l in enumerate(lines, 1):
    if re.match(r'^\s*```', l): fence += 1
    if re.search(r'<style\b', l, re.I): style += 1
    if re.search(r'</style>', l, re.I): style -= 1
    if l.count('`') % 2:
        print(f'{n}: odd backticks: {l.strip()[:80]}')
    if re.sub(r'`[^`]*`|<[^>]*>', '', l).count('**') % 2:
        print(f'{n}: odd ** markers: {l.strip()[:80]}')
print(f'code fences balanced: {fence % 2 == 0};  <style> balanced: {style == 0}')
PY
```

### 5. Spelling sweeps

The deck is **American English** throughout. Both lists below should come back empty except for
the deliberate entries noted.

```bash
python - <<'PY'
import re
s = open('src/slides.md', encoding='utf-8').read()
NEVER = {'our','your','four','hour','tour','pour','wise','otherwise','precise','noise','promise',
         'rise','advise','expertise','concise','likewise','premise','raise','praise','revise',
         'flour','supervise','surprise','comprise','arise','devise','franchise'}
brit = sorted({w for w in re.findall(r'\b[a-z]+\b', s)
               if re.search(r'(ise|isation|our)$', w) and w not in NEVER})
dbl = sorted(set(re.findall(r'\b(\w+) \1\b', s)))
print('British spellings :', brit or 'none')
print('doubled words     :', dbl or 'none', '  (billion, etc are deliberate)')
PY
```

### 6. Image references

```bash
miss=0
for r in $(grep -o 'images/[A-Za-z0-9._/-]*' src/slides.md | sort -u); do
  [ -f "src/$r" ] || { echo "MISSING: $r"; miss=1; }
done
[ $miss -eq 0 ] && echo "all $(grep -o 'images/[A-Za-z0-9._/-]*' src/slides.md | sort -u | wc -l) referenced images present"

echo "--- on disk but unreferenced (fine if work-in-progress) ---"
comm -23 <(find src/images -type f | sed 's|^src/||' | sort) \
         <(grep -o 'images/[A-Za-z0-9._/-]*' src/slides.md | sort -u)
```

Unreferenced images ship to GitHub Pages, so a large pile is worth moving to `files/unused-images/`
rather than leaving under `src/images/`.

### 7. Speaker-note markers

A note marker must be a bare `####` on its own line. `#### Some text` is silently ignored by
`make_notes.py`, so the note disappears from `notes.json` with no error.

```bash
grep -n '^####[[:space:]]\+[^[:space:]]' src/slides.md || echo "all note markers are bare ####"
```

### 8. col-N parity

The one genuine duplication in the build: `.cols > .col-N` weights are defined **twice** — in
`src/layout.css` for the slideshow, and again inside `scripts/make_readable.py` for the readable
page, which never loads `layout.css` by design. Adding a `col-9` to one and not the other makes
that slide render with the wrong split on one output only, silently.

```bash
python - <<'PY'
import re
used = set(re.findall(r'class="col-(\d)"', open('src/slides.md', encoding='utf-8').read()))
lay  = set(re.findall(r'\.col-(\d) \{', open('src/layout.css', encoding='utf-8').read()))
rd   = {a or b for a, b in re.findall(r'\.col-(\d)\) \{|> \.col-(\d) \{',
                                      open('scripts/make_readable.py', encoding='utf-8').read())}
print('used in slides.md :', sorted(used))
print('layout.css missing:', sorted(used - lay - {"1"}) or 'none')
print('readable  missing :', sorted(used - rd  - {"1"}) or 'none')
PY
```

`col-1` needs no rule — `.cols > *` already defaults to `flex: 1`.

### 9. Soft-break merges

`.marprc.yml` sets `breaks: false`, so consecutive prose lines join into one paragraph in **both**
outputs. That's usually what you want; this flags where it might not be.

```bash
python - <<'PY'
import re
lines = open('src/slides.md', encoding='utf-8').read().split('\n')
in_style = depth = 0; prev = None; runs = []
for n, l in enumerate(lines, 1):
    s = l.strip()
    if re.search(r'<style', s, re.I): in_style = 1
    if in_style:
        if re.search(r'</style>', s, re.I): in_style = 0
        prev = None; continue
    if s.startswith('<div'): depth += 1
    if s.startswith('</div'): depth = max(0, depth - 1)
    plain = (s and not s.startswith(('<', '#')) and s != '&nbsp;'
             and not re.match(r'^([-*+]|\d+[.)])\s', s)
             and not re.match(r'^ {0,3}([-*_])( *\1){2,} *$', s))
    if plain and not depth:
        hard = s.endswith('<br>') or l.endswith('  ')
        if prev is not None and not prev[1]: runs.append((prev[0], n))
        prev = (n, hard)
    else:
        prev = None
merged = []
for a, b in runs:
    if merged and merged[-1][1] == a: merged[-1] = (merged[-1][0], b)
    else: merged.append([a, b])
for a, b in merged:
    print(f'lines {a}-{b} join into one paragraph:')
    for i in range(a, b + 1): print(f'   {i}: {lines[i-1][:88]}')
print(f'{len(merged)} run(s)')
PY
```

**Expected hits (not bugs):** the YAML frontmatter at the top, and the multi-line `<iframe …>`
opening tag on the tokenspree slide. Anything else: add `<br>` at the end of the first line for a
hard break, or a blank line to make separate paragraphs.

---

## Tier 2 — build and structure

### 10. Full build

Order matters: `make_notes.py` reads and modifies `presentation.html`, so it runs last.

```bash
marp src/slides.md --html --theme src/marp-theme.css --output public/presentation.html
cp src/layout.css public/layout.css
scripts/build-readable.sh --no-open
python scripts/make_notes.py src/slides.md public/presentation.html public/notes.json
cp src/notes.html public/notes.html
mkdir -p public/tokenspree && cp -r demo/tokenspree/. public/tokenspree/
```

**`make_notes.py` is the regression test.** It parses slides from the markdown with its own
splitter and compares that against the `<section>` count Marp actually produced, failing loudly on
a mismatch:

```
ERROR: parsed 344 slides from src/slides.md but public/presentation.html contains 343
       — the slide splitter has drifted from Marp's actual behavior.
```

Nine times out of ten that means a **stale build** — you edited `slides.md` after building. Re-run
`marp` and try again. If it persists, the splitter in `make_notes.py` genuinely disagrees with Marp
and needs fixing.

### 11. TOC anchors

```bash
python - <<'PY'
import re
h = open('public/index.html', encoding='utf-8').read()
nav = re.search(r'<nav class="toc">.*?</nav>', h, re.DOTALL)
if not nav:
    print('!! no TOC in the readable page'); raise SystemExit
anchors = re.findall(r'href="#([^"]+)"', nav.group(0))
ids = set(re.findall(r'\bid="([^"]+)"', h))
broken = [a for a in anchors if a not in ids]
print(f'{len(anchors)} entries; broken: {broken or "none"}')
PY
```

### 12. Link parity across the outputs

```bash
echo "source  : $(grep -c '^- \[.*youtu\.be' src/slides.md)"
echo "slides  : $(grep -o '<a href="https://youtu\.be/' public/presentation.html | wc -l)"
echo "readable: $(grep -o '<a href="https://youtu\.be/' public/index.html | wc -l)"
echo "--- these three should match ---"
echo "payload : $(du -sh public | cut -f1)"
```

---

## Tier 3 — occasional

### 13. Visual spot-check

Slides are `overflow: hidden`, so content that grows past the slide is **clipped silently** — only
a screenshot catches it. Check the densest slides after any layout or CSS change.

```bash
# find the densest slides
python - <<'PY'
import re
h = open('public/presentation.html', encoding='utf-8').read()
d = []
for sid, body in re.findall(r'<section id="(\d+)"[^>]*>(.*?)</section>', h, re.DOTALL):
    vis = body.split('<h4')[0]
    d.append((len(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', vis))), int(sid)))
print('densest:', ' '.join(str(s) for _, s in sorted(d, reverse=True)[:6]))
PY

cd public && python -m http.server 8799 --bind 127.0.0.1 & sleep 2; cd ..
```

Then, from PowerShell (Chrome is a Windows binary — the path is easiest there):

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
foreach ($n in 27,63,156,296) {
  & $chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars `
    --user-data-dir="$env:TEMP\shot$n" --window-size=1280,720 --virtual-time-budget=12000 `
    --screenshot="$env:TEMP\slide-$n.png" "http://127.0.0.1:8799/presentation.html#$n"
}
```

Open the PNGs and look. Stop the server afterwards:

```bash
kill %1 2>/dev/null || true
```

### 14. Refresh YouTube link metadata

Run when links are added, to fetch canonical title, channel and duration. It caches, so re-running
only fetches what's new. Prints the annotated line for each link — paste in, or adapt to rewrite
`slides.md` directly.

```bash
python - <<'PY'
import json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')   # channel names contain non-cp1252 chars
CACHE = 'files/temp/yt_meta.json'
H = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'CONSENT=YES+cb'}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30).read().decode('utf-8', 'replace')

def hms(sec):
    h, rem = divmod(sec, 3600); m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'

src = open('src/slides.md', encoding='utf-8').read()
ids = sorted(set(re.findall(r'youtu\.be/([A-Za-z0-9_-]+)', src)))
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}
for vid in ids:
    if cache.get(vid, {}).get('duration'):
        continue
    try:
        o = json.loads(get(f'https://www.youtube.com/oembed?url=https://youtu.be/{vid}&format=json'))
        page = get(f'https://www.youtube.com/watch?v={vid}')
        secs = re.search(r'"lengthSeconds":"(\d+)"', page)
        cache[vid] = {'title': o['title'], 'channel': o['author_name'],
                      'duration': hms(int(secs.group(1))) if secs else None}
        print(f'  fetched {vid}: {cache[vid]["channel"]} ({cache[vid]["duration"]})')
    except Exception as e:
        print(f'  FAILED {vid}: {e}')
    time.sleep(0.4)
os.makedirs('files/temp', exist_ok=True)
json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('\n--- annotated lines ---')
for vid in ids:
    d = cache.get(vid, {})
    if d.get('duration'):
        print(f'- [{d["title"]}](https://youtu.be/{vid}) - {d["channel"]} ({d["duration"]})')
PY
```

---

## Known false positives

Verified against the rendered output — do not re-investigate these:

| Looks like | Actually |
|---|---|
| `[ARC 2026]`, `[The Perceptron]`, `[How Models Learn Part 3]` flagged as bracketed text | Balanced nested brackets inside link text, which CommonMark allows. They render as proper anchors. |
| `` `<repo-name>` `` flagged as an unknown HTML tag | Inside backticks, so it's code, not markup. |
| `</iframe>` reported without a matching open tag | The `<iframe class="game"` opening tag spans several lines; line-based scanners can't see it. |
| YAML frontmatter and `<style>` lines flagged by check 9 | Not prose; they never render as paragraphs. |
| `billion billion`, `etc etc` flagged as doubled words | Deliberate. |

---

## Environment gotchas

- **`marp` hangs.** Intermittent, and it's a stray `node` process, not the deck. Clear it from
  PowerShell with `Stop-Process -Name node -Force`, then re-run — a normal build takes ~1.5s.
- **Run `scripts/build-readable.sh` from git-bash, not PowerShell.** From PowerShell, `bash`
  resolves to WSL, where the `markdown` package isn't installed, and the build fails with
  `ModuleNotFoundError: No module named 'markdown'`.
- **`python3` doesn't exist here** — it's a Microsoft Store stub. Use `python`. (The scripts already
  handle this.)
- **`src/slides.md` is CRLF.** Any script matching line endings needs `\r\n`; reading with
  `newline=''` preserves them, and writing back with `newline=''` avoids reformatting the file.
- **An open editor can silently overwrite edits.** VS Code writing its buffer has reverted
  scripted edits to `slides.md` mid-session more than once. After a scripted change, re-read the
  file to confirm it stuck, and reload the editor before typing further.
- **`public/` is generated and git-ignored** — delete it any time; `scripts/README.md` has the full
  build.
