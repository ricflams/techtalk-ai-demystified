# PDF Format Experiment: Token Cost & Quality Comparison

**Hypothesis:** Converting PDFs to markdown before sending to Claude saves tokens and may
or may not affect quality, depending on PDF type.

**Approaches compared:**
- **Raw PDF** — PDF uploaded directly via the Anthropic document API (Claude extracts internally)
- **pymupdf4llm** — Converted to markdown on the command line, sent as text
- **marker** — ML-based markdown conversion (better table/layout handling), sent as text
- **pdftotext** — Plain text extraction, for token baseline only

---

## 1. Token Counts

| Document | Raw PDF | pymupdf4llm | pdftotext | MD/PDF ratio |
|----------|--------:|------------:|----------:|:------------:|
| Attention Is All You Need |  34,587 |      12,220 |    12,808 |     35%      |
| Deep Residual Learning for Image Recog |  37,427 |      20,433 |    21,683 |     55%      |
| Language Models are Few-Shot Learners  | 186,513 |      79,951 |    73,337 |     43%      |
| IRS Form 1040 (US Individual Income Ta |   6,694 |       8,588 |     4,466 |     128%     |
| NIST SP 800-145: The NIST Definition o |  13,210 |       2,387 |     2,445 |     18%      |
| NIST Cybersecurity Framework 1.1 | 123,717 |      41,283 |    42,059 |     33%      |
| BERT: Pre-training of Deep Bidirection |  43,929 |      19,728 |    21,809 |     45%      |
| Efficient Estimation of Word Represent |  16,550 |       6,057 |     6,092 |     37%      |
| Learning Transferable Visual Models Fr | 145,407 |      74,909 |    84,171 |     52%      |
| Generative Adversarial Nets (Goodfello |  22,262 |       9,121 |     8,878 |     41%      |
| **TOTAL** | **630,296** | **274,677** | **277,748** | **44%** |

> **Note:** The `count_tokens` API endpoint was used — no inference charges incurred.
> The "dummy question" added ~15 tokens to each measurement and is consistent across comparisons.


## 2. Quality Comparison (LLM-as-Judge, methodology v2)

Judge model: `claude-opus-5` · Scores: accuracy + completeness vs. a verified ground-truth reference answer, 1–5 each, averaged. Judge never sees which arm produced which candidate; candidate order is randomized per question.


| Document | Risk | PDF avg | pymupdf4llm avg | marker avg | Winner (PDF vs best MD) | MD tool winner |
|----------|:----:|:-------:|:---------------:|:----------:|:-----------------------:|:--------------:|
| Attention Is All You Need | high | — | — | — | not judged | — |
| Deep Residual Learning for Image Recog | high | — | — | — | not judged | — |
| Language Models are Few-Shot Learners  | high | — | — | — | not judged | — |
| IRS Form 1040 (US Individual Income Ta | high | — | — | — | not judged | — |
| NIST SP 800-145: The NIST Definition o | low | 5.0/5 | 5.0/5 | 5.0/5 | **tie** (0-0-10) | tie |
| NIST Cybersecurity Framework 1.1 | high | — | — | — | not judged | — |
| BERT: Pre-training of Deep Bidirection | high | — | — | — | not judged | — |
| Efficient Estimation of Word Represent | low | — | — | — | not judged | — |
| Learning Transferable Visual Models Fr | high | — | — | — | not judged | — |
| Generative Adversarial Nets (Goodfello | high | — | — | — | not judged | — |

**Overall (PDF vs. best-of-markdown):** PDF wins: 0, Markdown wins: 0, Ties: 10

**Significance (sign test, excluding ties):** n/a (no non-tie comparisons)


**Stratified — low extraction-risk docs (plain text):** PDF 0 / MD 0 / tie 10 — n/a (no non-tie comparisons)

**Stratified — high extraction-risk docs (tables/equations/figures/layout):** PDF 0 / MD 0 / tie 0 — n/a (no non-tie comparisons)


**Markdown converter comparison (pymupdf4llm vs. marker):** marker wins: 0, pymupdf4llm wins: 0, ties: 10 — n/a (no non-tie comparisons)


## 3. Methodology v2 changes from the original run

- **Ground truth**: judge now scores each candidate against a verified reference answer
  (`build_ground_truth.py`, derived from the raw PDF only) instead of purely comparing
  candidates to each other.
- **Blind, randomized judging**: the judge is never told which arm produced which answer,
  and candidate order is shuffled per question — v1's judge prompt explicitly labeled
  "Answer A (from raw PDF)" / "Answer B (from converted markdown)" with PDF always first.
- **Stronger, symmetric model**: both the answering model and the judge model were upgraded
  from Sonnet-answers/Haiku-judges to the same strong model, so neither is stronger than
  the other or than what it's grading.
- **Third arm — marker**: added `marker` as a second, higher-quality markdown conversion
  alongside `pymupdf4llm`'s default settings, so "raw PDF vs. markdown" is tested against
  best-effort markdown, not just one converter's defaults.
- **Significance testing**: an exact two-sided binomial (sign) test on non-tie comparisons,
  computed overall and stratified by each document's `extraction_risk` tag (plain text vs.
  tables/equations/figures/layout), so the effect isn't averaged away across dissimilar
  document types.

See `results/v1_original/` for the original run's answers/scores/report, preserved for comparison.
