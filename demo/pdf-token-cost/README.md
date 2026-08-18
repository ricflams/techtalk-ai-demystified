# Experiment: PDF raw vs. converted-to-markdown

**Hypothesis to test:** Is it better to convert a PDF to markdown before sending it to an
LLM, or to upload the raw PDF and let the API extract it?

**What we measure:**
1. Token cost for each approach (using the free `count_tokens` API endpoint)
2. Answer quality on 10 factual questions per PDF (LLM-as-judge scoring)

---

## The 10 PDFs

| # | Document | Type | Why it's interesting |
|---|----------|------|----------------------|
| 1 | Attention Is All You Need | Academic + math | Equations, attention diagrams |
| 2 | ResNet | Academic + figures | Many images and result tables |
| 3 | GPT-3 | Academic + large | ~75 pages, dense tables |
| 4 | IRS Form 1040 | Form / layout | 2 pages but complex positional layout |
| 5 | GPL v3 | Legal text | Dense plain text, well-structured |
| 6 | NIST Cybersecurity Framework | Gov. report | ~55 pages, structured categories |
| 7 | BERT | Academic | Tables, architecture diagrams |
| 8 | Word2Vec | Academic + small | ~12 pages, mostly text |
| 9 | CLIP | Academic + images | 48 pages, extremely image-heavy |
| 10 | GANs (Goodfellow) | Academic + math | 9 pages, theory-heavy |

---

## Setup

```bash
# 1. Install dependencies
bash setup.sh

# 2. Set your API keys
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...     # only for the OpenAI legs (steps 3 and 7)
export GEMINI_API_KEY=...        # only for the Gemini legs (steps 3 and 7)
```

> **WSL2 note:** Use `python3` instead of `python` unless you've run `sudo apt install python-is-python3`.

---

## Running the experiment

### Step 1 — Download PDFs (no API key needed)
```bash
python3 download.py
```

### Step 2 — Convert to markdown using three tools
```bash
python3 convert.py
```

This runs:
- **pdftotext** (poppler) — plain text baseline, no formatting
- **pymupdf4llm** — markdown with headings, tables, some formatting preserved
- **marker** — ML-based, best quality (skipped if not installed; `pip install marker-pdf`)

### Step 3 — Count tokens (free for Anthropic; the others cost a little)
```bash
python3 measure_tokens.py           # Anthropic count_tokens — free, no inference
python3 measure_tokens_openai.py    # OpenAI: real call for raw PDF, tiktoken for markdown
python3 measure_tokens_gemini.py    # Gemini count_tokens
```
Measures token cost for raw PDF via the document API, pymupdf4llm markdown, and
pdftotext plain text. Writes `results/tokens.json`, `tokens_openai.json`, `tokens_gemini.json`.

### Step 4 — Build the ground-truth answer key (~$1–2)
```bash
python3 build_ground_truth.py

# Specific PDFs, or a different model
python3 build_ground_truth.py --pdf attention gans
python3 build_ground_truth.py --model claude-opus-5
```

Reads each **raw** PDF (never the markdown conversions, so question/answer phrasing isn't
biased toward one extraction method) and produces a reference answer + supporting verbatim
quote + confidence label for all 10 questions per document. Writes `results/ground_truth.json`.

**`report.py --judge` hard-fails without this file** — the judge grades both arms against it
rather than against each other. Resumable: re-running skips documents already built, so use
`--force` to regenerate. Spot-check the equations, exact numbers, and any `low` confidence
flags before trusting it as the reference.

### Step 5 — Run QA experiment (~$3–5 at Sonnet pricing)
```bash
python3 run_qa.py

# Quick test: first 2 questions only, specific PDFs
python3 run_qa.py --limit 2 --pdf attention gans

# Use a different model
python3 run_qa.py --model claude-haiku-4-5-20251001    # cheaper, ~$0.30 total
```

Each question is asked twice: once with raw PDF, once with markdown. Answers are saved
to `results/answers/{pdf_id}/q{N}_{approach}.txt`.

### Step 6 — Generate report
```bash
# Without quality scoring (just token table)
python3 report.py

# With LLM-as-judge quality scoring against ground_truth.json (~$0.50 extra)
python3 report.py --judge
```

Output: `results/report.md`, `results/scores.json`. The previous methodology's run is kept
at `results/v1_original/` for comparison.

### Step 7 — Verify the token numbers (optional, ~$1)

Each provider's headline number came from a different kind of measurement, so each needs its
own cross-check against real billed usage:

```bash
python3 verify_claude.py    # count_tokens dry-run vs. real messages.create billing
python3 verify_gemini.py    # count_tokens vs. real usage + end-of-document questions
python3 verify_openai.py    # tiktoken estimate vs. real call; truncation; figure comprehension
```

Written to `results/verify_{claude,gemini,openai}.json`. `verify_claude.py` exists because
Claude's `raw_pdf` figure was the one number produced *only* by the free `count_tokens`
endpoint and never compared against a real billed call.

---

## Best converter for Linux command line

| Tool | Install | Quality | Speed | Handles images |
|------|---------|---------|-------|----------------|
| `pdftotext` | `sudo apt install poppler-utils` | baseline text | very fast | no |
| `pymupdf4llm` | `pip install pymupdf4llm` | good markdown | fast | no |
| `marker` | `pip install marker-pdf` | best (ML) | slow (GPU helps) | yes (described) |
| `docling` | `pip install docling` | excellent | moderate | yes |

**Recommended for most use cases:** `pymupdf4llm` — one pip install, no model downloads,
produces clean markdown with headers and tables.

**Best possible:** `marker-pdf` — ML-based, handles equations, tables, mixed layouts.
Requires ~2GB model download. GPU optional but speeds things up significantly.

Command-line usage:
```bash
# pymupdf4llm (Python one-liner)
python3 -c "import pymupdf4llm; print(pymupdf4llm.to_markdown('file.pdf'))" > file.md

# marker
marker_single file.pdf --output_dir ./output --output_format markdown

# pdftotext
pdftotext -layout file.pdf file.txt
```

---

## What to expect

| PDF type | Token cost (MD vs raw) | Quality difference |
|----------|----------------------|-------------------|
| Dense text (GPL, Word2Vec) | MD ~60% cheaper | None |
| Academic with figures | MD ~40% cheaper | Minor (missing images) |
| Image-heavy (CLIP) | MD ~70% cheaper | Notable (figures lost) |
| Forms (IRS 1040) | MD ~50% cheaper | Notable (layout lost) |
| Large with tables (GPT-3) | MD ~50% cheaper | Minor (table formatting) |

The key insight: API providers **do not** ingest raw binary PDF bytes into the token stream.
They extract content server-side — but they do it **page-by-page as images**, which is why
raw PDFs cost more tokens and preserve visual layout better.
