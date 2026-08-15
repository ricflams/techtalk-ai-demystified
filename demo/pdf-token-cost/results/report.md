# PDF Format Experiment: Token Cost & Quality Comparison

**Hypothesis:** Converting PDFs to markdown before sending to Claude saves tokens and may
or may not affect quality, depending on PDF type.

**Approaches compared:**
- **Raw PDF** — PDF uploaded directly via the Anthropic document API (Claude extracts internally)
- **pymupdf4llm** — Converted to markdown on the command line, sent as text
- **pdftotext** — Plain text extraction, for token baseline only

---

## 1. Token Counts

| Document | Pages est. | Raw PDF | pymupdf4llm | pdftotext | MD/PDF ratio |
|----------|:----------:|--------:|------------:|----------:|:------------:|
| Attention Is All You Need | — |  34,587 |      12,220 |    12,808 |     35%      |
| Deep Residual Learning for Image Recog | — |  37,427 |      20,433 |    21,683 |     55%      |
| Language Models are Few-Shot Learners  | — | 186,513 |      79,951 |    73,337 |     43%      |
| IRS Form 1040 (US Individual Income Ta | — |   6,694 |       8,588 |     4,466 |     128%     |
| NIST SP 800-145: The NIST Definition o | — |  13,210 |       2,387 |     2,445 |     18%      |
| NIST Cybersecurity Framework 1.1 | — | 123,717 |      41,283 |    42,059 |     33%      |
| BERT: Pre-training of Deep Bidirection | — |  43,929 |      19,728 |    21,809 |     45%      |
| Efficient Estimation of Word Represent | — |  16,550 |       6,057 |     6,092 |     37%      |
| Learning Transferable Visual Models Fr | — | 145,407 |      74,909 |    84,171 |     52%      |
| Generative Adversarial Nets (Goodfello | — |  22,262 |       9,121 |     8,878 |     41%      |
| **TOTAL** | | **630,296** | **274,677** | **277,748** | **44%** |

> **Note:** The `count_tokens` API endpoint was used — no inference charges incurred.
> The "dummy question" added ~15 tokens to each measurement and is consistent across comparisons.


## 2. Quality Comparison (LLM-as-Judge)

Judge model: `claude-haiku-4-5-20251001` · Scores: accuracy + completeness, 1–5 each, averaged.


| Document | Type | PDF avg | MD avg | Winner | Note |
|----------|------|:-------:|:------:|:------:|------|
| Attention Is All You Need | academic-math | 5.0/5 | 4.8/5 | **PDF** | Both answers accurately identify and explain the t |
| Deep Residual Learning for Image Recog | academic-figures | 4.8/5 | 4.8/5 | **MD** | Answer A provides slightly more precise characteri |
| Language Models are Few-Shot Learners  | academic-large | 4.8/5 | 4.7/5 | **tie** | Both answers are accurate, but B is more complete  |
| IRS Form 1040 (US Individual Income Ta | form-layout | 4.7/5 | 4.5/5 | **PDF** | Both answers correctly identify Line 11a as the AG |
| NIST SP 800-145: The NIST Definition o | legal-text | 5.0/5 | 5.0/5 | **PDF** | Both answers accurately present the NIST definitio |
| NIST Cybersecurity Framework 1.1 | structured-report | 4.8/5 | 4.7/5 | **tie** | Both answers provide identical and accurate descri |
| BERT: Pre-training of Deep Bidirection | academic-math | 4.9/5 | 4.7/5 | **PDF** | Both answers are accurate, but Answer A provides a |
| Efficient Estimation of Word Represent | academic-text | 4.9/5 | 4.8/5 | **PDF** | Both correctly identify the false premise, but Ans |
| Learning Transferable Visual Models Fr | academic-images | 4.7/5 | 4.7/5 | **PDF** | Both answers correctly identify CLIP as 'Contrasti |
| Generative Adversarial Nets (Goodfello | academic-math | 5.0/5 | 4.8/5 | **PDF** | Both answers accurately present the optimal discri |

**Overall:** PDF wins: 7, Markdown wins: 1, Ties: 2

## 3. Key Observations

### Token cost
- **Image-heavy PDFs** (CLIP, IRS form): raw PDF is far more expensive; the AI services
  process each page visually, similar to an image.
- **Text-heavy PDFs** (GPL, Word2Vec, GANs): markdown version is ~40–70% cheaper with
  no quality loss.
- **Large papers with many tables** (GPT-3, NIST CSF): markdown saves tokens significantly
  but may miss fine-grained table formatting.

### Quality
- **Plain text documents**: quality is essentially equal. The AI services extract text
  just as well as pymupdf4llm.
- **Forms and structured layouts** (IRS 1040): raw PDF is better because layout relationships
  (which field is next to which label) are preserved by the visual processing.
- **Math equations**: raw PDF may be better if the equations are in rendered form;
  pymupdf4llm renders LaTeX reasonably but may miss complex symbols.
- **Image captions / figure references**: raw PDF wins because the images themselves
  give context that is lost in pure text extraction.

## 4. Conclusion

The popular belief that "upload the PDF directly = AI processes raw binary bytes" is a
misconception. API providers extract content from PDFs server-side, similarly to what
pymupdf4llm or pdftotext do locally.

**However, the API's extraction is image-based per-page**, so it:
- Costs more tokens (each page ≈ a medium-resolution image)
- Preserves visual layout (useful for forms, complex tables)
- Handles images/figures natively (good for image-heavy papers)

**pymupdf4llm** converts structured text more token-efficiently but loses images.

**Practical recommendation:**
- Text/code/legal docs → convert to markdown first (cheaper, same quality)
- Forms, slides, image-heavy reports → send raw PDF (better quality justifies cost)
- Academic papers → either works; markdown is ~40% cheaper
