#!/usr/bin/env python3
"""
Run the QA experiment: ask 10 questions per PDF using two approaches.
  A) raw PDF sent directly to Claude via the document API
  B) pymupdf4llm markdown sent as text

(A third `marker` arm was attempted for higher-quality markdown conversion but is
impractical on this machine: GPU OOMs even at fp16 on the 4GB card, and CPU-only
conversion takes 1hr+ per document. Dropped — see findings.md.)

The same model answers both arms so the model upgrade doesn't itself introduce
asymmetry between arms.

Answers saved to results/answers/{pdf_id}/q{N}_{approach}.txt
Usage:
  python run_qa.py                          # all PDFs, all questions
  python run_qa.py --limit 3               # first 3 questions only (quick test)
  python run_qa.py --pdf attention bert    # specific PDFs
  python run_qa.py --model claude-opus-5
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import anthropic

CATALOG        = Path(__file__).parent / "pdfs.json"
PDFS_DIR       = Path(__file__).parent / "pdfs"
MD_DIR         = Path(__file__).parent / "markdown" / "pymupdf4llm"
ANSWERS_DIR    = Path(__file__).parent / "results" / "answers"

DEFAULT_MODEL = "claude-opus-5"
MAX_TOKENS    = 2048  # opus-5 writes noticeably longer structured answers than sonnet did;
                      # 1024 truncated multi-part answers (e.g. "list the five characteristics") mid-sentence


def extract_text(resp) -> str:
    """claude-opus-5 sometimes emits a thinking block (text=None) as content[0] even with
    thinking disabled server-side in rare cases — never assume content[0] is the answer."""
    for block in resp.content:
        if block.type == "text":
            return block.text
    raise ValueError(f"No text block in response: {resp.content}")


def usage_dict(resp) -> dict:
    """Cached tokens are billed separately from usage.input_tokens (uncached input only) —
    record all three so token/cost accounting stays accurate once caching is in play."""
    u = resp.usage
    return {
        "input_tokens":              u.input_tokens,
        "output_tokens":             u.output_tokens,
        "cache_creation_input_tokens": u.cache_creation_input_tokens,
        "cache_read_input_tokens":     u.cache_read_input_tokens,
    }


def ask_with_pdf(client, pdf_path: Path, question: str, model: str) -> tuple[str, dict]:
    # The same PDF is re-sent for all 10 questions on this document — mark it as an
    # ephemeral cache breakpoint so questions 2-10 hit a ~90%-cheaper cache read instead
    # of repaying full input-token price for the whole document each time.
    data = base64.standard_b64encode(pdf_path.read_bytes()).decode()
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
                    "cache_control": {"type": "ephemeral"},
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return extract_text(resp), usage_dict(resp)


def ask_with_markdown(client, md_text: str, question: str, model: str) -> tuple[str, dict]:
    resp = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": f"<document>\n{md_text}\n</document>", "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": question},
            ],
        }],
    )
    return extract_text(resp), usage_dict(resp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit",  type=int, default=None, help="Max questions per PDF")
    parser.add_argument("--pdf",    nargs="+",              help="PDF IDs to run (default: all)")
    parser.add_argument("--model",  default=DEFAULT_MODEL)
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set"); sys.exit(1)

    client  = anthropic.Anthropic()
    catalog = json.loads(CATALOG.read_text())
    ANSWERS_DIR.mkdir(parents=True, exist_ok=True)

    if args.pdf:
        catalog = [e for e in catalog if e["id"] in args.pdf]
        if not catalog:
            print(f"No matching PDFs for: {args.pdf}"); sys.exit(1)

    total_questions = sum(len(e["questions"][:args.limit or 99]) for e in catalog)
    print(f"Model: {args.model}")
    print(f"PDFs: {len(catalog)}  Questions per PDF: up to {args.limit or 10}  Total API calls: {total_questions * 2}\n")

    for entry in catalog:
        pdf_path        = PDFS_DIR / entry["filename"]
        pymupdf_path    = MD_DIR / (entry["filename"].replace(".pdf", ".md"))
        out_dir         = ANSWERS_DIR / entry["id"]
        out_dir.mkdir(exist_ok=True)

        if not pdf_path.exists():
            print(f"SKIP {entry['id']}: PDF not downloaded"); continue

        arms = [("pdf", ask_with_pdf, pdf_path)]
        if pymupdf_path.exists():
            arms.append(("markdown_pymupdf4llm", ask_with_markdown,
                         pymupdf_path.read_text(encoding="utf-8", errors="replace")))
        else:
            print(f"  {entry['id']}: pymupdf4llm markdown not converted, skipping that arm")

        questions = entry["questions"][:args.limit]

        print(f"\n{'='*60}")
        print(f"  {entry['name']}")
        print(f"  PDF: {pdf_path.stat().st_size//1024} KB")
        print(f"{'='*60}")

        for i, question in enumerate(questions, 1):
            print(f"\n  Q{i}: {question[:70]}…" if len(question) > 70 else f"\n  Q{i}: {question}")

            for approach, func, arg in arms:
                out_file = out_dir / f"q{i:02d}_{approach}.txt"
                meta_file = out_dir / f"q{i:02d}_{approach}.meta.json"

                if out_file.exists():
                    print(f"    {approach:22}: SKIP (already done)")
                    continue

                try:
                    answer, usage = func(client, arg, question, args.model)
                    out_file.write_text(answer, encoding="utf-8")
                    meta_file.write_text(json.dumps({
                        "question": question,
                        "approach": approach,
                        "model":    args.model,
                        **usage,
                    }), encoding="utf-8")
                    billed_in = usage["input_tokens"] + usage["cache_creation_input_tokens"] + usage["cache_read_input_tokens"]
                    print(f"    {approach:22}: {billed_in:,} in "
                          f"(cache write {usage['cache_creation_input_tokens']:,} / read {usage['cache_read_input_tokens']:,}) "
                          f"/ {usage['output_tokens']:,} out")
                    time.sleep(0.5)  # polite rate limiting
                except anthropic.RateLimitError:
                    print(f"    {approach:22}: rate limited — waiting 30s…")
                    time.sleep(30)
                except Exception as e:
                    print(f"    {approach:22}: ERROR: {e}")

    print(f"\n\nDone. Answers in {ANSWERS_DIR}/")


if __name__ == "__main__":
    main()
