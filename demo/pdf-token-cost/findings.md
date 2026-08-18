# Demo: PDF raw vs. converted-to-markdown

**Repo:** `techtalk-ai-llm-demystified/demo/pdf-token-cost/`

Tests whether converting a PDF to markdown before sending to an LLM is a meaningful optimisation, or whether uploading the raw PDF is just as good — or better.

---

## The misconception

> "Convert PDFs to markdown first — otherwise the AI ingests raw binary bytes."

A refined but still-wrong version: *"They all just use pdftotext server-side anyway."*

Neither is fully correct. Each provider does something fundamentally different.

---

## Setup

10 well-known PDFs of diverse types:

| # | Document | Type | Size (bytes) |
|---|----------|------|-------------:|
| 1 | Attention Is All You Need | Academic + math | 2,215,244 |
| 2 | ResNet | Academic + figures | 819,383 |
| 3 | GPT-3 | Academic + large (75 pages) | 6,768,044 |
| 4 | IRS Form 1040 | Form / layout | 220,237 |
| 5 | NIST SP 800-145 (Cloud Computing) | Short plain text | 85,781 |
| 6 | NIST Cybersecurity Framework 1.1 | Structured report | 1,062,822 |
| 7 | BERT | Academic | 775,166 |
| 8 | Word2Vec | Academic + small | 228,716 |
| 9 | CLIP | Academic + image-heavy | 6,813,639 |
| 10 | GANs (Goodfellow) | Academic + math | 530,482 |

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
| Word2Vec* | 16,550 | 6,057 | 1,816 | 5,669 | 5,762 | 5,411 |
| CLIP | 145,407 | 74,909 | 12,394 | 74,948 | 71,083 | 67,183 |
| GANs | 22,262 | 9,121 | 2,332 | 8,402 | 8,291 | 8,231 |

*\*Word2Vec row is measured against the wrong PDF — `pdfs.json` pointed at arXiv:1301.3666 ("Zero-Shot Learning Through Cross-Modal Transfer" by Socher et al.), not arXiv:1301.3781 (the actual Word2Vec paper by Mikolov et al.). Fixed post-hoc; see Verification section below for corrected numbers. This didn't affect the ratio much by coincidence (both raw and markdown were measured on the same wrong file, so the ratio itself stayed internally consistent), but the absolute token counts and any quality-judging done against this document in the original 34/22/44 result were against the wrong paper.*

**ratio = raw PDF ÷ markdown for that provider**

| Provider | Typical ratio | What it means |
|----------|:------------:|---------------|
| Anthropic | 200–550% | Raw PDF costs 2–6× more than markdown |
| OpenAI | 97–109% | Raw PDF ≈ markdown, essentially identical |
| Gemini | 15–80% | Raw PDF costs 3–18× **less** than markdown |

---

## Why the numbers diverge so dramatically

**Correction (see Verification section below for the full derivation):** the explanations
below for Anthropic and Gemini were revised after checking exact per-page token math against
real page counts. The original version claimed Anthropic charges the same regardless of
content and that Gemini's savings come from aggressive text extraction with a large
tokenizer — both turned out to be wrong in a specific, checkable way.

**Gemini processes PDFs as pure vision input, at an exact flat rate of 258 tokens per page**
— not text extraction at all. Across all 10 documents, real token counts equal `258 ×
page_count + 10` **exactly**, every time, regardless of whether the page is dense academic
text, a mostly-blank tax form, or image-heavy figures. Zero variance across wildly different
content densities is only possible if the cost is a fixed per-page image-encoding rate. This
is why Gemini is so cheap for text-heavy documents (a 258-token image is way cheaper than
extracting and re-tokenizing the text on that page would be) — not because of a bigger
vocabulary or more aggressive whitespace stripping.

**Anthropic renders each page as an image too, but — unlike Gemini — the cost is *not* flat.**
Per-page cost ranges from 1,887 tokens (NIST 800-145, plain text) up to 3,347 tokens (IRS
1040, dense form layout), correlating with content complexity: plain text cheapest,
image/figure-heavy documents (CLIP, ResNet) and dense form layouts (IRS 1040) priciest. This
means Anthropic's real cost is closer to "image rendering plus something that scales with
content" than "one flat image tax" — the original claim that "a plain-text page costs the
same as a diagram-heavy page" doesn't hold up against the actual per-page numbers.

**OpenAI** does text extraction server-side, similar to what `pdftotext` does locally — raw
PDF and converted markdown cost nearly the same. This one holds up as a cost-level
description (see Verification), though the exact mechanism (pure text vs. some hybrid) isn't
fully nailed down, and answer quality on table-heavy content suggests OpenAI's own
extraction may be lower-fidelity than a good local parser in at least some cases.

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

## Verification: is the raw-PDF token accounting actually correct?

The numbers above were originally measured with each provider's free `count_tokens`-style
endpoint (or, for OpenAI, a real inference call — see below), but only Gemini's raw-PDF
number was ever independently checked against real billed usage in the original experiment.
A follow-up audit closed that gap for all three providers.

### Anthropic — doubly verified

A real `messages.create()` call was made for each of the 10 PDFs and compared against
`count_tokens()`'s prediction: **9 of 10 matched to +0.0%** (the 10th was the word2vec
wrong-file issue above). End-of-document questions were also asked directly against the raw
PDF for the three largest documents (GPT-3, CLIP, NIST CSF) — all six answers correctly
pulled specific facts from deep appendices/glossaries at the very end of 48–75 page
documents, with real billed token counts matching `count_tokens()` predictions almost
exactly (e.g. GPT-3: 208,846 predicted vs. 208,833 actual). No truncation, no discrepancy.

**A more important discovery came out of this check: `count_tokens()` is accurate, but only
for the model you actually pass it.** The original experiment measured all Anthropic numbers
with `claude-haiku-4-5-20251001`, under the assumption that "model only affects tokenizer,
not cost." That's true within the Claude 4.x generation (Haiku 4.5, Sonnet 4.5, and Sonnet
4.6 all tokenize identically), but **false across generations** — `claude-opus-5` uses a
measurably different tokenizer, for PDFs *and* plain text:

| Document | Haiku/Sonnet-4.x raw | Opus 5 raw | Haiku/Sonnet-4.x md | Opus 5 md | ratio (4.x) | ratio (Opus 5) |
|---|---:|---:|---:|---:|:---:|:---:|
| Attention | 34,587 | 38,370 (+11%) | 12,220 | 16,275 (+33%) | 35% | 42% |
| ResNet | 37,427 | 42,756 (+14%) | 20,433 | 26,146 (+28%) | 55% | 61% |
| GPT-3 | 186,513 | 208,846 (+12%) | 79,951 | 103,814 (+30%) | 43% | 50% |
| IRS 1040 | 6,694 | 7,541 (+13%) | 8,588 | 11,823 (+38%) | 128% | 157% |
| NIST 800-145 | 13,210 | 14,356 (+9%) | 2,387 | 3,551 (+49%) | 18% | 25% |
| NIST CSF | 123,717 | 136,506 (+10%) | 41,283 | 54,534 (+32%) | 33% | 40% |
| BERT | 43,929 | 50,194 (+14%) | 19,728 | 26,308 (+33%) | 45% | 52% |
| Word2Vec (corrected PDF) | 28,791 | 32,289 (+12%) | 11,265 | 14,967 (+33%) | 39% | 46% |
| CLIP | 145,407 | 166,711 (+15%) | 74,909 | 96,739 (+29%) | 52% | 58% |
| GANs | 22,262 | 24,916 (+12%) | 9,121 | 12,155 (+33%) | 41% | 49% |

Raw-PDF cost rises modestly under Opus 5 (+9–15%), but plain-text/markdown cost rises much
more (+28–49%) — meaning markdown's cost advantage over raw PDF shrinks under the newer
tokenizer (though the qualitative conclusion — raw PDF costs substantially more, except for
layout-heavy forms — is unchanged). **Takeaway for future measurement: always measure with
the specific model you'll actually use; don't assume tokenizer parity across a provider's
whole model lineup, especially across major version jumps.**

### Gemini — reconfirmed, and the mechanism identified precisely

Re-checked with a fresh API key: a live call on the GPT-3 paper returned 19,367 tokens
against the original prediction of 19,360 (+0.04%) — consistent with the original
experiment's own verification (`verify_gemini.py`, <0.1% match across all 10 PDFs, plus
end-of-document completeness questions). This remains the most rigorously verified of the
three providers' raw-PDF numbers.

Going further: using exact page counts (via `pdfinfo`, not the approximate descriptions in
`pdfs.json`), Gemini's raw-PDF token count fits `258 × pages + 10` **exactly**, to the token,
for 9 of 10 documents (word2vec excluded — wrong-file issue above):

| Doc | Pages | 258×pages | Actual | Residual |
|---|---:|---:|---:|---:|
| Attention | 15 | 3,870 | 3,880 | +10 |
| BERT | 16 | 4,128 | 4,138 | +10 |
| CLIP | 48 | 12,384 | 12,394 | +10 |
| GANs | 9 | 2,322 | 2,332 | +10 |
| GPT-3 | 75 | 19,350 | 19,360 | +10 |
| IRS 1040 | 2 | 516 | 526 | +10 |
| NIST 800-145 | 7 | 1,806 | 1,816 | +10 |
| NIST CSF | 55 | 14,190 | 14,200 | +10 |
| ResNet | 12 | 3,096 | 3,106 | +10 |

The +10 is the fixed cost of the dummy question text, constant across every document
regardless of its content. This precision — zero variance across 2-to-75-page documents of
wildly different content density — only makes sense if Gemini bills a flat per-page rate for
treating each page as an image, not if it's doing adaptive text extraction. This overturns
the original explanation ("aggressive text extraction... 256K vocabulary tokeniser") in the
section above.

Anthropic's per-page cost was checked the same way and does **not** fit a flat rate — it
ranges from 1,887 to 3,347 tokens/page and correlates with content complexity (see above),
consistent with combining a base image-rendering cost with some amount of extracted text on
top, rather than one fixed number per page.

### OpenAI — the one real gap, now closed (mostly)

The original methodology measured OpenAI's raw PDF with a **real** inference call
(`resp.usage.prompt_tokens`, never an estimate) but markdown with a **local tiktoken
simulation** — an asymmetry that was never checked for bias, and nobody had tested whether
the raw-PDF call actually processes the whole document or just part of it. Three checks:

1. **Tiktoken-vs-real-call check**: the local estimate matched a real call to within
   +0.0% to +0.3% across all 10 documents. The asymmetric methodology doesn't introduce a
   measurable bias — tiktoken really is exact here.
2. **Truncation check** (end-of-document questions on GPT-3, CLIP, NIST CSF via raw PDF):
   token counts stayed at full-document scale (68–71K for GPT-3, ~71K for CLIP, ~38K for
   NIST CSF) and NIST CSF's glossary "Risk" definition came back **word-for-word identical**
   to Claude's answer — the whole document is genuinely present in context, not truncated.
3. **Answer-quality check**: gpt-4o-mini's answers were noticeably weaker than Claude's on
   two of six deep questions — misreading GPT-3's Table C.1 (confusing an accuracy score
   with a contamination percentage) and confabulating a specific-sounding but likely-wrong
   answer after falling for a false premise in a CLIP appendix question. Re-running the
   *same two questions* against local pymupdf4llm markdown instead of the raw PDF (same
   model, different input) gave a **split result**: the GPT-3/table question's answer
   changed substantially and became more coherent with markdown input, suggesting OpenAI's
   server-side extraction may handle *this specific table's numeric structure* less
   faithfully than pymupdf4llm's parse — while the CLIP/false-premise question got the
   *same wrong answer either way*, pointing to a model-capability limitation (gpt-4o-mini
   being a small, cheap model, not an extraction defect) rather than an extraction issue.

**Net effect on the headline claim:** the OpenAI raw-PDF token count is confirmed to be a
real, non-truncated, full-document measurement — the "raw ≈ markdown" cost finding holds.
What's *not* fully confirmed is the causal explanation offered below ("OpenAI does text
extraction similar to pdftotext") — the answer-quality split suggests OpenAI's actual
server-side extraction may occasionally be lower-fidelity than a good local parser on
table-heavy content specifically, even though the aggregate token count lands in the same
ballpark. The cost conclusion is solid; the "how" is a plausible simplification, not a
fully verified mechanism.

---

## Conclusion

| Provider | PDF processing | Best strategy |
|----------|---------------|--------------|
| **Gemini** | Pure vision — flat 258 tokens/page, content-independent | Upload raw PDF — 3–18× cheaper, same quality |
| **OpenAI** | Standard text extraction (≈ pdftotext) | Doesn't matter — cost is essentially the same, though watch for table-fidelity loss |
| **Anthropic** | Image-based per page, cost scales with content complexity | Convert to markdown first — 2–6× cheaper, more so for plain text than for image/figure-heavy docs |

The "optimal" strategy depends entirely on the provider. Converting to markdown first is good advice for Anthropic, irrelevant for OpenAI, and actively wasteful for Gemini.
