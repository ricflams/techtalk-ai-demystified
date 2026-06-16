#!/usr/bin/env python3
"""
Count tokens for each PDF using the Gemini API — raw PDF vs markdown.

Requires: pip install google-genai
API key:  https://aistudio.google.com/apikey
          export GEMINI_API_KEY=...
"""
import json
import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: run: pip install google-genai")
    sys.exit(1)

CATALOG     = Path(__file__).parent / "pdfs.json"
PDFS_DIR    = Path(__file__).parent / "pdfs"
MD_DIR      = Path(__file__).parent / "markdown"
RESULTS_DIR = Path(__file__).parent / "results"

DUMMY_Q = "What is the main topic of this document?"
MODEL   = "gemini-2.5-flash"


def count_pdf_tokens(client, pdf_path: Path) -> int:
    uploaded = client.files.upload(
        file=str(pdf_path),
        config=types.UploadFileConfig(mime_type="application/pdf"),
    )
    for _ in range(30):
        f = client.files.get(name=uploaded.name)
        if str(f.state).endswith("ACTIVE"):
            break
        time.sleep(2)

    result = client.models.count_tokens(
        model=MODEL,
        contents=[uploaded, DUMMY_Q],
    )
    client.files.delete(name=uploaded.name)
    return result.total_tokens


def count_text_tokens(client, text: str) -> int:
    wrapped = f"<document>\n{text}\n</document>\n\n{DUMMY_Q}"
    result = client.models.count_tokens(model=MODEL, contents=wrapped)
    return result.total_tokens


def read_text(pdf_stem: str, tool: str, suffix: str = ".md") -> str | None:
    path = MD_DIR / tool / (pdf_stem + suffix)
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else None


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        print("Get one at: https://aistudio.google.com/apikey")
        sys.exit(1)

    client  = genai.Client(api_key=api_key)
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(exist_ok=True)

    results_file = RESULTS_DIR / "tokens_gemini.json"
    results = json.loads(results_file.read_text()) if results_file.exists() else {}

    for entry in catalog:
        pdf_id   = entry["id"]
        pdf_stem = entry["filename"].replace(".pdf", "")
        pdf_path = PDFS_DIR / entry["filename"]
        rec      = results.get(pdf_id, {})
        changed  = False

        if not pdf_path.exists():
            print(f"SKIP {entry['name'][:40]}: not downloaded")
            continue

        print(f"\n  {entry['name'][:60]}")

        if "raw_pdf" not in rec:
            print(f"    uploading + counting raw PDF…", end=" ", flush=True)
            try:
                rec["raw_pdf"] = count_pdf_tokens(client, pdf_path)
                changed = True
                print(f"{rec['raw_pdf']:,}")
            except Exception as e:
                print(f"ERROR: {e}")
                rec["raw_pdf"] = None

        for tool, suffix in [("pymupdf4llm", ".md"), ("pdftotext", ".txt")]:
            if tool not in rec:
                text = read_text(pdf_stem, tool, suffix)
                if text:
                    print(f"    counting {tool}…", end=" ", flush=True)
                    try:
                        rec[tool] = count_text_tokens(client, text)
                        changed = True
                        print(f"{rec[tool]:,}")
                    except Exception as e:
                        print(f"ERROR: {e}")
                        rec[tool] = None

        rec["name"] = entry["name"]
        rec["type"] = entry["type"]
        results[pdf_id] = rec
        if changed:
            results_file.write_text(json.dumps(results, indent=2))

    # ── side-by-side comparison table ────────────────────────────────────────
    anthropic_file = RESULTS_DIR / "tokens.json"
    anthropic = json.loads(anthropic_file.read_text()) if anthropic_file.exists() else {}

    print(f"\n\n{'Document':<40} {'── Anthropic ──':^26} {'── Gemini ──':^26}")
    print(f"{'':40} {'raw':>8} {'muPDF':>8} {'ratio':>7}   {'raw':>8} {'muPDF':>8} {'ratio':>7}")
    print("-" * 100)

    for entry in catalog:
        pid = entry["id"]
        a   = anthropic.get(pid, {})
        g   = results.get(pid, {})

        a_raw, a_md = a.get("raw_pdf"), a.get("pymupdf4llm")
        g_raw, g_md = g.get("raw_pdf"), g.get("pymupdf4llm")

        a_ratio = f"{a_md/a_raw:.0%}" if a_raw and a_md else "—"
        g_ratio = f"{g_md/g_raw:.0%}" if g_raw and g_md else "—"

        print(
            f"  {entry['name'][:38]:<38}"
            f"  {f'{a_raw:,}' if a_raw else '—':>8}"
            f"  {f'{a_md:,}'  if a_md  else '—':>8}"
            f"  {a_ratio:>6}"
            f"   {f'{g_raw:,}' if g_raw else '—':>8}"
            f"  {f'{g_md:,}'  if g_md  else '—':>8}"
            f"  {g_ratio:>6}"
        )

    print(f"\nGemini results saved to {results_file}")


if __name__ == "__main__":
    main()
