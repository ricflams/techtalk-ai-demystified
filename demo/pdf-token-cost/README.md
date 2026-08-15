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

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...
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

### Step 3 — Count tokens (free, no inference)
```bash
python3 measure_tokens.py
```
Uses the Anthropic `count_tokens` endpoint. Measures token cost for:
- Raw PDF via document API
- pymupdf4llm markdown
- pdftotext plain text

### Step 4 — Run QA experiment (~$3–5 at Sonnet pricing)
```bash
python3 run_qa.py

# Quick test: first 2 questions only, specific PDFs
python3 run_qa.py --limit 2 --pdf attention gans

# Use a different model
python3 run_qa.py --model claude-haiku-4-5-20251001    # cheaper, ~$0.30 total
```

Each question is asked twice: once with raw PDF, once with markdown. Answers are saved
to `results/answers/{pdf_id}/q{N}_{approach}.txt`.

### Step 5 — Generate report
```bash
# Without quality scoring (just token table)
python3 report.py

# With LLM-as-judge quality scoring (~$0.50 extra)
python3 report.py --judge
```

Output: `results/report.md`

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
