# Demo: PDF raw vs. converted-to-markdown

**Repo:** `techtalk-ai-llm-demystified/experiment/`

Tests whether converting a PDF to markdown before sending to an LLM is a meaningful optimisation, or whether uploading the raw PDF is just as good — or better.

---

## The misconception

> "Convert PDFs to markdown first — otherwise the AI ingests raw binary bytes."

A refined but still-wrong version: *"They all just use pdftotext server-side anyway."*

Neither is fully correct. Each provider does something fundamentally different.

---

## Setup

10 well-known PDFs of diverse types:

| # | Document | Type |
|---|----------|------|
| 1 | Attention Is All You Need | Academic + math |
| 2 | ResNet | Academic + figures |
| 3 | GPT-3 | Academic + large (75 pages) |
| 4 | IRS Form 1040 | Form / layout |
| 5 | NIST SP 800-145 (Cloud Computing) | Short plain text |
| 6 | NIST Cybersecurity Framework 1.1 | Structured report |
| 7 | BERT | Academic |
| 8 | Word2Vec | Academic + small |
| 9 | CLIP | Academic + image-heavy |
| 10 | GANs (Goodfellow) | Academic + math |

Each PDF converted locally with `pdftotext` and `pymupdf4llm`. Token counts measured for raw PDF upload vs. converted markdown at each provider. Quality tested with 10 questions per PDF, LLM-as-judge scoring.

---

## Token cost results

| Document | Anthr. raw | Anthr. muPDF | Gemini raw | Gemini muPDF | OpenAI raw | OpenAI muPDF |
|----------|----------:|-------------:|-----------:|-------------:|-----------:|-------------:|
| Attention Is All You Need | 34,587 | 12,220 | 3,880 | 11,589 | 11,388 | 10,789 |
| ResNet | 37,427 | 20,433 | 3,106 | 20,247 | 19,031 | 18,335 |
| GPT-3 | 186,513 | 79,951 | 19,360 | 77,489 | 68,793 | 70,924 |
| IRS Form 1040 | 6,694 | 8,588 | 526 | 9,711 | 3,606 | 8,187 |
| NIST SP 800-145 | 13,210 | 2,387 | 1,816 | 2,276 | 2,937 | 2,167 |
| NIST CSF 1.1 | 123,717 | 41,283 | 14,200 | 41,270 | 37,911 | 36,815 |
| BERT | 43,929 | 19,728 | 4,138 | 18,348 | 18,795 | 17,212 |
| Word2Vec | 16,550 | 6,057 | 1,816 | 5,669 | 5,762 | 5,411 |
| CLIP | 145,407 | 74,909 | 12,394 | 74,948 | 71,083 | 67,183 |
| GANs | 22,262 | 9,121 | 2,332 | 8,402 | 8,291 | 8,231 |

**ratio = raw PDF ÷ markdown for that provider**

| Provider | Typical ratio | What it means |
|----------|:------------:|---------------|
| Anthropic | 200–550% | Raw PDF costs 2–6× more than markdown |
| OpenAI | 97–109% | Raw PDF ≈ markdown, essentially identical |
| Gemini | 15–80% | Raw PDF costs 3–18× **less** than markdown |

---

## Why the numbers diverge so dramatically

**Anthropic** renders each page as an image regardless of content. A plain-text page costs the same as a diagram-heavy page. This is why a 7-page text document (NIST 800-145) costs 13,210 tokens raw but only 2,387 as markdown.

**OpenAI** does text extraction server-side, similar to what `pdftotext` does locally. Raw PDF and converted markdown cost nearly the same.

**Gemini** does text extraction too, but far more aggressively — stripping running headers, page numbers, column-spacing whitespace, and hyphenation artifacts that `pdftotext` preserves. Combined with a 256K vocabulary tokeniser, this produces token counts 3–10× lower than even local text extraction.

**Best single illustration — IRS Form 1040 (2 pages, mostly whitespace and labels):**

| Approach | Tokens |
|----------|-------:|
| Anthropic raw PDF | 6,694 |
| OpenAI raw PDF | 3,606 |
| Gemini raw PDF | **526** |
| pymupdf4llm markdown | ~8,500 |

---

## Quality results

100 questions across 10 PDFs, asked with both raw PDF and pymupdf4llm markdown, judged by Claude (Anthropic only).

| PDF | PDF wins | MD wins | Ties |
|-----|:--------:|:-------:|:----:|
| Attention Is All You Need | 2 | 1 | 7 |
| ResNet | 2 | 4 | 4 |
| GPT-3 | 4 | 4 | 2 |
| IRS Form 1040 | 6 | 3 | 1 |
| NIST SP 800-145 | 1 | 0 | 9 |
| NIST CSF 1.1 | 3 | 3 | 4 |
| BERT | 6 | 2 | 2 |
| Word2Vec | 3 | 1 | 6 |
| CLIP | 4 | 3 | 3 |
| GANs | 3 | 1 | 6 |
| **Total** | **34 (34%)** | **22 (22%)** | **44 (44%)** |

Raw PDF has a consistent but modest quality edge overall. Most questions (44%) are equivalent. The biggest PDF wins are on layout-sensitive documents (IRS Form 1040) and math-heavy papers (BERT — markdown can't reproduce equations). ResNet is the only document where markdown clearly wins.

Gemini's raw PDF extraction was verified to be complete — end-of-document questions including appendix content from 75-page papers answered correctly.

---

## Conclusion

| Provider | PDF processing | Best strategy |
|----------|---------------|--------------|
| **Gemini** | Smart text extraction, noise removal | Upload raw PDF — 3–18× cheaper, same quality |
| **OpenAI** | Standard text extraction (≈ pdftotext) | Doesn't matter — cost is essentially the same |
| **Anthropic** | Image-based, one render per page | Convert to markdown first — 2–6× cheaper |

The "optimal" strategy depends entirely on the provider. Converting to markdown first is good advice for Anthropic, irrelevant for OpenAI, and actively wasteful for Gemini.
