#!/usr/bin/env python3
"""
Count tokens for each PDF in three forms:
  - raw PDF (as Claude receives it via the document API)
  - pymupdf4llm markdown
  - pdftotext plain text

Uses the Anthropic count_tokens endpoint — no inference charges.
Results saved to results/tokens.json and printed as a table.
"""
import base64
import json
import os
import sys
from pathlib import Path

import anthropic

CATALOG = Path(__file__).parent / "pdfs.json"
PDFS_DIR = Path(__file__).parent / "pdfs"
MD_DIR = Path(__file__).parent / "markdown"
RESULTS_DIR = Path(__file__).parent / "results"

# A short dummy question to make the message realistic
DUMMY_Q = "What is the main topic of this document?"

MODEL = "claude-haiku-4-5-20251001"  # model only affects tokenizer, not cost here


def count_pdf_tokens(client: anthropic.Anthropic, pdf_path: Path) -> int:
    data = base64.standard_b64encode(pdf_path.read_bytes()).decode()
    resp = client.messages.count_tokens(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "base64", "media_type": "application/pdf", "data": data},
                },
                {"type": "text", "text": DUMMY_Q},
            ],
        }],
    )
    return resp.input_tokens


def count_text_tokens(client: anthropic.Anthropic, text: str) -> int:
    wrapped = f"<document>\n{text}\n</document>\n\n{DUMMY_Q}"
    resp = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": wrapped}],
    )
    return resp.input_tokens


def read_markdown(pdf_id: str, tool: str, suffix: str = ".md") -> str | None:
    path = MD_DIR / tool / (pdf_id + suffix)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic()
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(exist_ok=True)

    token_file = RESULTS_DIR / "tokens.json"
    results = json.loads(token_file.read_text()) if token_file.exists() else {}

    print(f"{'Document':<40} {'Raw PDF':>10} {'pymupdf4llm':>13} {'pdftotext':>11}")
    print("-" * 78)

    for entry in catalog:
        pdf_id = entry["id"]
        pdf_path = PDFS_DIR / entry["filename"]
        rec = results.get(pdf_id, {})
        changed = False

        if not pdf_path.exists():
            print(f"  {'SKIP':>6}  {entry['name'][:40]} — not downloaded")
            continue

        # Raw PDF
        if "raw_pdf" not in rec:
            print(f"  counting raw PDF for {entry['name'][:40]}…", end=" ", flush=True)
            try:
                rec["raw_pdf"] = count_pdf_tokens(client, pdf_path)
                changed = True
                print(f"{rec['raw_pdf']:,}")
            except Exception as e:
                print(f"ERROR: {e}")
                rec["raw_pdf"] = None

        # pymupdf4llm
        if "pymupdf4llm" not in rec:
            md = read_markdown(entry["filename"].replace(".pdf", ""), "pymupdf4llm")
            if md:
                print(f"  counting pymupdf4llm for {entry['name'][:30]}…", end=" ", flush=True)
                try:
                    rec["pymupdf4llm"] = count_text_tokens(client, md)
                    changed = True
                    print(f"{rec['pymupdf4llm']:,}")
                except Exception as e:
                    print(f"ERROR: {e}")
                    rec["pymupdf4llm"] = None
            else:
                rec["pymupdf4llm"] = None

        # pdftotext
        if "pdftotext" not in rec:
            txt = read_markdown(entry["filename"].replace(".pdf", ""), "pdftotext", ".txt")
            if txt:
                print(f"  counting pdftotext for {entry['name'][:30]}…", end=" ", flush=True)
                try:
                    rec["pdftotext"] = count_text_tokens(client, txt)
                    changed = True
                    print(f"{rec['pdftotext']:,}")
                except Exception as e:
                    print(f"ERROR: {e}")
                    rec["pdftotext"] = None
            else:
                rec["pdftotext"] = None

        rec["name"] = entry["name"]
        rec["type"] = entry["type"]
        results[pdf_id] = rec
        if changed:
            token_file.write_text(json.dumps(results, indent=2))

    # Summary table
    print(f"\n{'Document':<40} {'Raw PDF':>10} {'pymupdf4llm':>13} {'pdftotext':>11}  {'muPDF ratio':>12}")
    print("-" * 92)
    for pid, rec in results.items():
        raw = rec.get("raw_pdf")
        mupdf = rec.get("pymupdf4llm")
        ptxt = rec.get("pdftotext")
        ratio = f"{mupdf/raw:.1%}" if raw and mupdf else "—"
        raw_s   = f"{raw:,}"   if raw   else "—"
        mupdf_s = f"{mupdf:,}" if mupdf else "—"
        ptxt_s  = f"{ptxt:,}"  if ptxt  else "—"
        print(f"  {rec['name'][:38]:<38} {raw_s:>10} {mupdf_s:>13} {ptxt_s:>11}  {ratio:>12}")

    print(f"\nResults saved to {token_file}")


if __name__ == "__main__":
    main()
