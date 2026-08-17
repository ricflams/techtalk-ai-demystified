#!/usr/bin/env python3
"""
Generate the experiment report.

Reads:
  results/tokens.json        — token counts from measure_tokens.py
  results/ground_truth.json  — verified reference answers from build_ground_truth.py
  results/answers/           — QA answers from run_qa.py (pdf / markdown_pymupdf4llm / markdown_marker)

Optionally runs LLM-as-judge to score answer quality (--judge flag).

Methodology v2 (see findings.md for the full writeup of what changed and why):
  - Judge scores each candidate's accuracy/completeness against a verified ground-truth
    reference answer, rather than purely comparing candidates to each other.
  - Candidate order is randomized and unlabeled (the judge never sees which arm produced
    which answer) to remove the source-label bias in v1.
  - Judge model upgraded to match the answering model's strength.
  - Three arms compared: raw PDF, pymupdf4llm markdown, marker markdown. The primary
    comparison is PDF vs. best-of-the-two-markdowns per question ("best-effort markdown"),
    with a secondary comparison of which markdown converter wins.
  - Aggregate win/loss counts get an exact two-sided binomial test (excluding ties),
    computed overall and stratified by each document's `extraction_risk` tag.

Output: results/report.md
"""
import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

import anthropic
from scipy.stats import binomtest

CATALOG       = Path(__file__).parent / "pdfs.json"
RESULTS_DIR   = Path(__file__).parent / "results"
ANSWERS_DIR   = RESULTS_DIR / "answers"
TOKENS_FILE   = RESULTS_DIR / "tokens.json"
GT_FILE       = RESULTS_DIR / "ground_truth.json"
SCORES_FILE   = RESULTS_DIR / "scores.json"
REPORT_FILE   = RESULTS_DIR / "report.md"

JUDGE_MODEL = "claude-opus-5"
ARMS = ["pdf", "markdown_pymupdf4llm", "markdown_marker"]
ARM_LABEL = {"pdf": "Raw PDF", "markdown_pymupdf4llm": "pymupdf4llm", "markdown_marker": "marker"}

JUDGE_PROMPT_HEADER = """\
You are a neutral judge scoring candidate answers to a question about a document, against \
a verified reference answer. You are not told how any candidate answer was produced — judge \
each purely on its own merits against the reference.

The question is: {question}

Reference answer (verified correct): {reference}

Score each candidate from 1 to 5 on:
- accuracy: does the candidate agree with the reference answer's facts (numbers, terms, \
equations, names, etc.), penalizing incorrect, hallucinated, or missing details?
- completeness: does it fully address the question the way the reference answer does?

"""

JUDGE_PROMPT_FOOTER = """
Respond with valid JSON only, no prose: a single JSON object with one key per candidate \
(matching the candidate numbers above) plus a "note" key, shaped like:
{example}"""


def extract_text(resp) -> str:
    """claude-opus-5 can emit a thinking block (text=None) as content[0] even with
    thinking disabled server-side in rare cases — never assume content[0] is the answer."""
    for block in resp.content:
        if block.type == "text":
            return block.text
    raise ValueError(f"No text block in response: {resp.content}")


def parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def judge(client, question: str, reference: str, candidates: dict[str, str]) -> dict:
    """candidates: {arm_name: answer_text}, at least 2 entries.
    Returns {arm_name: {"accuracy": N, "completeness": N}, "note": str}."""
    arm_names = list(candidates.keys())
    order = arm_names[:]
    random.shuffle(order)  # order[i] = real arm name shown as "Candidate i+1"

    blocks = "\n".join(
        f"Candidate {i+1}:\n{candidates[order[i]][:2000]}\n" for i in range(len(order))
    )
    example = "{" + ", ".join(f'"c{i+1}_accuracy": N, "c{i+1}_completeness": N' for i in range(len(order))) \
              + ', "note": "one sentence explanation"}'
    prompt = JUDGE_PROMPT_HEADER.format(question=question, reference=reference[:2000]) \
              + blocks + JUDGE_PROMPT_FOOTER.format(example=example)

    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=400,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": prompt}],
    )
    parsed = parse_json_response(extract_text(resp))

    result = {"note": parsed.get("note", "")}
    for i, arm_name in enumerate(order, 1):
        result[arm_name] = {
            "accuracy":     parsed[f"c{i}_accuracy"],
            "completeness": parsed[f"c{i}_completeness"],
        }
    return result


def load_answers(pdf_id: str, q_idx: int) -> dict[str, str]:
    d = ANSWERS_DIR / pdf_id
    out = {}
    for arm in ARMS:
        f = d / f"q{q_idx:02d}_{arm}.txt"
        if f.exists():
            out[arm] = f.read_text(encoding="utf-8", errors="replace")
    return out


def run_judging(client, catalog: list, ground_truth: dict) -> dict:
    scores = json.loads(SCORES_FILE.read_text()) if SCORES_FILE.exists() else {}

    for entry in catalog:
        pdf_id = entry["id"]
        if pdf_id not in scores:
            scores[pdf_id] = {}
        gt_for_doc = ground_truth.get(pdf_id, {})

        for i, question in enumerate(entry["questions"], 1):
            key = f"q{i:02d}"
            if key in scores[pdf_id]:
                continue

            candidates = load_answers(pdf_id, i)
            if len(candidates) < 2:
                continue  # need at least 2 arms to compare

            gt_entry = gt_for_doc.get(key)
            if not gt_entry:
                print(f"  SKIP {pdf_id} Q{i}: no ground truth available")
                continue

            print(f"  judging {pdf_id} Q{i}…", end=" ", flush=True)
            try:
                result = judge(client, question, gt_entry["answer"], candidates)
                result["reference_confidence"] = gt_entry.get("confidence")
                scores[pdf_id][key] = result
                print({arm: result[arm] for arm in candidates})
                SCORES_FILE.write_text(json.dumps(scores, indent=2))
                time.sleep(0.3)
            except Exception as e:
                print(f"ERROR: {e}")

    return scores


def arm_avg(qscore: dict, arm: str) -> float | None:
    if arm not in qscore:
        return None
    return (qscore[arm]["accuracy"] + qscore[arm]["completeness"]) / 2


def primary_winner(qscore: dict) -> str | None:
    """PDF vs. best-of-markdown (pymupdf4llm/marker) for this question."""
    pdf_score = arm_avg(qscore, "pdf")
    md_scores = [s for s in (arm_avg(qscore, "markdown_pymupdf4llm"), arm_avg(qscore, "markdown_marker")) if s is not None]
    if pdf_score is None or not md_scores:
        return None
    md_best = max(md_scores)
    if pdf_score > md_best:
        return "pdf"
    if md_best > pdf_score:
        return "markdown"
    return "tie"


def markdown_tool_winner(qscore: dict) -> str | None:
    a, b = arm_avg(qscore, "markdown_pymupdf4llm"), arm_avg(qscore, "markdown_marker")
    if a is None or b is None:
        return None
    if a > b:
        return "pymupdf4llm"
    if b > a:
        return "marker"
    return "tie"


def sign_test(wins: int, losses: int) -> str:
    n = wins + losses
    if n == 0:
        return "n/a (no non-tie comparisons)"
    result = binomtest(wins, n, 0.5)
    return f"p={result.pvalue:.3f} (n={n} non-tie comparisons, {wins}-{losses})"


def format_tokens_table(tokens: dict, catalog: list) -> str:
    rows = ["| Document | Raw PDF | pymupdf4llm | pdftotext | MD/PDF ratio |",
            "|----------|--------:|------------:|----------:|:------------:|"]

    for entry in catalog:
        pid = entry["id"]
        rec = tokens.get(pid, {})
        raw   = rec.get("raw_pdf")
        mupdf = rec.get("pymupdf4llm")
        ptxt  = rec.get("pdftotext")
        ratio = f"{mupdf/raw:.0%}" if raw and mupdf else "—"
        rows.append(
            f"| {entry['name'][:38]} "
            f"| {f'{raw:,}' if raw else '—':>7} "
            f"| {f'{mupdf:,}' if mupdf else '—':>11} "
            f"| {f'{ptxt:,}' if ptxt else '—':>9} "
            f"| {ratio:^12} |"
        )

    tot_raw   = sum(v.get("raw_pdf", 0)      or 0 for v in tokens.values())
    tot_mupdf = sum(v.get("pymupdf4llm", 0)  or 0 for v in tokens.values())
    tot_ptxt  = sum(v.get("pdftotext", 0)    or 0 for v in tokens.values())
    tot_ratio = f"{tot_mupdf/tot_raw:.0%}" if tot_raw and tot_mupdf else "—"
    rows.append(f"| **TOTAL** | **{tot_raw:,}** | **{tot_mupdf:,}** | **{tot_ptxt:,}** | **{tot_ratio}** |")

    return "\n".join(rows)


def format_quality_table(scores: dict, catalog: list) -> tuple[str, dict]:
    rows = ["| Document | Risk | PDF avg | pymupdf4llm avg | marker avg | Winner (PDF vs best MD) | MD tool winner |",
            "|----------|:----:|:-------:|:---------------:|:----------:|:-----------------------:|:--------------:|"]

    totals = {
        "overall": {"pdf": 0, "markdown": 0, "tie": 0},
        "low":     {"pdf": 0, "markdown": 0, "tie": 0},
        "high":    {"pdf": 0, "markdown": 0, "tie": 0},
        "md_tool": {"pymupdf4llm": 0, "marker": 0, "tie": 0},
    }

    for entry in catalog:
        pid = entry["id"]
        risk = entry.get("extraction_risk", "?")
        qs = scores.get(pid, {})
        if not qs:
            rows.append(f"| {entry['name'][:38]} | {risk} | — | — | — | not judged | — |")
            continue

        pdf_avgs   = [arm_avg(v, "pdf") for v in qs.values() if arm_avg(v, "pdf") is not None]
        mupdf_avgs = [arm_avg(v, "markdown_pymupdf4llm") for v in qs.values() if arm_avg(v, "markdown_pymupdf4llm") is not None]
        marker_avgs = [arm_avg(v, "markdown_marker") for v in qs.values() if arm_avg(v, "markdown_marker") is not None]

        doc_pdf_wins = doc_md_wins = doc_ties = 0
        for v in qs.values():
            w = primary_winner(v)
            if w is None:
                continue
            totals["overall"][w] += 1
            totals[risk][w] = totals.get(risk, {}).get(w, 0) + 1
            if w == "pdf":
                doc_pdf_wins += 1
            elif w == "markdown":
                doc_md_wins += 1
            else:
                doc_ties += 1

            tw = markdown_tool_winner(v)
            if tw is not None:
                totals["md_tool"][tw] += 1

        winner = "PDF" if doc_pdf_wins > doc_md_wins else ("MD" if doc_md_wins > doc_pdf_wins else "tie")
        md_tool_wins = sum(1 for v in qs.values() if markdown_tool_winner(v) == "marker")
        md_tool_losses = sum(1 for v in qs.values() if markdown_tool_winner(v) == "pymupdf4llm")
        md_tool_summary = "marker" if md_tool_wins > md_tool_losses else ("pymupdf4llm" if md_tool_losses > md_tool_wins else "tie")

        def fmt(avgs):
            return f"{sum(avgs)/len(avgs):.1f}/5" if avgs else "—"

        rows.append(
            f"| {entry['name'][:38]} | {risk} "
            f"| {fmt(pdf_avgs)} | {fmt(mupdf_avgs)} | {fmt(marker_avgs)} "
            f"| **{winner}** ({doc_pdf_wins}-{doc_md_wins}-{doc_ties}) | {md_tool_summary} |"
        )

    return "\n".join(rows), totals


def build_report(catalog: list, tokens: dict, scores: dict) -> str:
    sections = []

    sections.append("""\
# PDF Format Experiment: Token Cost & Quality Comparison

**Hypothesis:** Converting PDFs to markdown before sending to Claude saves tokens and may
or may not affect quality, depending on PDF type.

**Approaches compared:**
- **Raw PDF** — PDF uploaded directly via the Anthropic document API (Claude extracts internally)
- **pymupdf4llm** — Converted to markdown on the command line, sent as text
- **marker** — ML-based markdown conversion (better table/layout handling), sent as text
- **pdftotext** — Plain text extraction, for token baseline only

---
""")

    sections.append("## 1. Token Counts\n")
    if tokens:
        sections.append(format_tokens_table(tokens, catalog))
        sections.append("""
> **Note:** The `count_tokens` API endpoint was used — no inference charges incurred.
> The "dummy question" added ~15 tokens to each measurement and is consistent across comparisons.
""")
    else:
        sections.append("_Run `python measure_tokens.py` to populate this section._\n")

    sections.append("\n## 2. Quality Comparison (LLM-as-Judge, methodology v2)\n")
    sections.append(
        f"Judge model: `{JUDGE_MODEL}` · Scores: accuracy + completeness vs. a verified ground-truth "
        f"reference answer, 1–5 each, averaged. Judge never sees which arm produced which candidate; "
        f"candidate order is randomized per question.\n\n"
    )
    if scores:
        table, totals = format_quality_table(scores, catalog)
        sections.append(table)

        o = totals["overall"]
        sections.append(f"\n**Overall (PDF vs. best-of-markdown):** PDF wins: {o['pdf']}, Markdown wins: {o['markdown']}, Ties: {o['tie']}")
        sections.append(f"\n**Significance (sign test, excluding ties):** {sign_test(o['pdf'], o['markdown'])}")

        low, high = totals.get("low", {}), totals.get("high", {})
        sections.append(f"\n\n**Stratified — low extraction-risk docs (plain text):** PDF {low.get('pdf',0)} / MD {low.get('markdown',0)} / tie {low.get('tie',0)} — {sign_test(low.get('pdf',0), low.get('markdown',0))}")
        sections.append(f"\n**Stratified — high extraction-risk docs (tables/equations/figures/layout):** PDF {high.get('pdf',0)} / MD {high.get('markdown',0)} / tie {high.get('tie',0)} — {sign_test(high.get('pdf',0), high.get('markdown',0))}")

        mt = totals["md_tool"]
        sections.append(f"\n\n**Markdown converter comparison (pymupdf4llm vs. marker):** marker wins: {mt['marker']}, pymupdf4llm wins: {mt['pymupdf4llm']}, ties: {mt['tie']} — {sign_test(mt['marker'], mt['pymupdf4llm'])}")
    else:
        sections.append("_Run `python run_qa.py` then `python report.py --judge` to populate this section._\n")

    sections.append("""\


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
""")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", action="store_true", help="Run LLM-as-judge scoring")
    args = parser.parse_args()

    if args.judge and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set"); sys.exit(1)

    catalog = json.loads(CATALOG.read_text())
    tokens  = json.loads(TOKENS_FILE.read_text()) if TOKENS_FILE.exists() else {}
    scores  = json.loads(SCORES_FILE.read_text()) if SCORES_FILE.exists() else {}

    if args.judge:
        ground_truth = json.loads(GT_FILE.read_text()) if GT_FILE.exists() else {}
        if not ground_truth:
            print("ERROR: results/ground_truth.json missing or empty — run build_ground_truth.py first"); sys.exit(1)
        client = anthropic.Anthropic()
        print("Running LLM-as-judge…")
        scores = run_judging(client, catalog, ground_truth)

    report = build_report(catalog, tokens, scores)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"\nReport written to {REPORT_FILE}")
    print("\n" + "="*60)
    print(report[:2000] + ("…" if len(report) > 2000 else ""))


if __name__ == "__main__":
    main()
