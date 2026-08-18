#!/usr/bin/env python3
"""
Build a verified ground-truth answer key for the QA experiment.

Reads each RAW PDF (never the markdown conversions, to avoid biasing question/answer
phrasing toward one extraction method) and asks a single strong model to answer all
10 questions for that document in one call, each with a supporting verbatim quote and
a confidence label. This is the reference the judge grades both arms against, and the
source-of-truth documentation for how the 100 questions' correct answers were derived
(previously undocumented).

Output: results/ground_truth.json, keyed by pdf_id -> "q01".."q10" -> {answer, quote, confidence}

Usage:
  python build_ground_truth.py                  # all PDFs
  python build_ground_truth.py --pdf attention   # specific PDFs
  python build_ground_truth.py --model claude-opus-5
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import anthropic

CATALOG      = Path(__file__).parent / "pdfs.json"
PDFS_DIR     = Path(__file__).parent / "pdfs"
RESULTS_DIR  = Path(__file__).parent / "results"
OUT_FILE     = RESULTS_DIR / "ground_truth.json"

DEFAULT_MODEL = "claude-opus-5"
MAX_TOKENS    = 4096
MAX_RETRIES   = 3

PROMPT_TEMPLATE = """\
You are building a verified answer key for a research experiment on PDF text extraction. \
You will be given the full raw PDF of a document and a numbered list of factual questions about it.

For each question, provide:
- "answer": the precise, correct answer based solely on this document's content. Be exact on \
numbers, equations, and technical parameters — do not round or approximate.
- "quote": an exact verbatim quote from the document that supports the answer (or the closest \
supporting passage if the question requires synthesizing a list/summary from multiple places).
- "confidence": "high" if the document unambiguously states this, "medium" if you had to \
synthesize/infer from multiple parts of the document, "low" if you are not fully sure or the \
document doesn't clearly contain the answer.

If the document does not contain enough information to answer confidently, say so plainly in \
"answer" and set confidence to "low" — do not guess or fill in from outside knowledge.

Questions:
{numbered_questions}

Respond with valid JSON only, no prose: a single JSON array (starting with "[" and ending \
with "]") of exactly {n} objects in question order, each shaped like:
{{"question_index": 1, "answer": "...", "quote": "...", "confidence": "high"|"medium"|"low"}}
Do not emit the objects as a bare comma-separated sequence outside of an enclosing array."""


def extract_text(resp) -> str:
    """claude-opus-5 can emit a thinking block (text=None) as content[0] even with
    thinking disabled server-side in rare cases — never assume content[0] is the answer."""
    for block in resp.content:
        if block.type == "text":
            return block.text
    raise ValueError(f"No text block in response: {resp.content}")


def parse_json_response(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        pass

    # Fallback: the model sometimes emits bare comma-separated objects without the
    # enclosing [ ]. Decode one JSON value at a time instead of failing outright.
    decoder = json.JSONDecoder()
    objects = []
    idx, n = 0, len(text)
    while idx < n:
        while idx < n and text[idx] in " \t\n\r,":
            idx += 1
        if idx >= n:
            break
        obj, end = decoder.raw_decode(text, idx)
        objects.append(obj)
        idx = end
    if not objects:
        raise ValueError(f"Could not parse any JSON objects from response: {text[:200]!r}")
    return objects


def build_ground_truth_for_pdf(client, pdf_path: Path, questions: list[str], model: str) -> list[dict]:
    numbered = "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1))
    prompt = PROMPT_TEMPLATE.format(numbered_questions=numbered, n=len(questions))
    data = base64.standard_b64encode(pdf_path.read_bytes()).decode()

    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=MAX_TOKENS,
                thinking={"type": "disabled"},
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {"type": "base64", "media_type": "application/pdf", "data": data},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }],
            )
            return parse_json_response(extract_text(resp))
        except anthropic.RateLimitError as e:
            last_err = e
            wait = 30 * (attempt + 1)
            print(f"    rate limited — waiting {wait}s…")
            time.sleep(wait)
        except anthropic.APIStatusError as e:
            last_err = e
            if e.status_code in (500, 502, 503, 529):
                wait = 15 * (attempt + 1)
                print(f"    {e.status_code} — retrying in {wait}s…")
                time.sleep(wait)
            else:
                raise
    raise last_err


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf",   nargs="+",              help="PDF IDs to run (default: all)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--force", action="store_true", help="Regenerate even if already present")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set"); sys.exit(1)

    client  = anthropic.Anthropic()
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ground_truth = json.loads(OUT_FILE.read_text()) if OUT_FILE.exists() else {}

    if args.pdf:
        catalog = [e for e in catalog if e["id"] in args.pdf]
        if not catalog:
            print(f"No matching PDFs for: {args.pdf}"); sys.exit(1)

    print(f"Model: {args.model}")
    print(f"PDFs: {len(catalog)}\n")

    for entry in catalog:
        pdf_id = entry["id"]
        pdf_path = PDFS_DIR / entry["filename"]

        if not pdf_path.exists():
            print(f"SKIP {pdf_id}: PDF not downloaded"); continue
        if pdf_id in ground_truth and not args.force:
            print(f"SKIP {pdf_id}: ground truth already built (use --force to regenerate)"); continue

        questions = entry["questions"]
        print(f"{'='*60}\n  {entry['name']}  ({len(questions)} questions)\n{'='*60}")

        try:
            results = build_ground_truth_for_pdf(client, pdf_path, questions, args.model)
            per_q = {}
            for r in results:
                key = f"q{r['question_index']:02d}"
                per_q[key] = {
                    "answer":     r["answer"],
                    "quote":      r.get("quote"),
                    "confidence": r.get("confidence"),
                }
            ground_truth[pdf_id] = per_q
            OUT_FILE.write_text(json.dumps(ground_truth, indent=2))
            low_conf = [k for k, v in per_q.items() if v["confidence"] == "low"]
            print(f"  done — {len(per_q)} answers" + (f"  (LOW CONFIDENCE: {', '.join(low_conf)})" if low_conf else ""))
        except Exception as e:
            print(f"  ERROR: {e}")

        time.sleep(0.5)

    print(f"\nGround truth written to {OUT_FILE}")
    print("Spot-check a handful (especially equations/exact numbers/low-confidence flags) before trusting this as the judge's reference.")


if __name__ == "__main__":
    main()
