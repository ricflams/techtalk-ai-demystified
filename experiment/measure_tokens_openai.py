#!/usr/bin/env python3
"""
Count tokens for each PDF using the OpenAI API — raw PDF vs markdown.

Requires: pip install openai tiktoken
API key:  https://platform.openai.com/api-keys
          export OPENAI_API_KEY=...

Raw PDF:  uploaded via Files API, one minimal inference call per PDF to read
          usage.prompt_tokens, then deleted. Cost: ~$0.01-0.05 total.
Markdown: counted locally with tiktoken (free, no API call).
"""
import json
import os
import sys
import time
from pathlib import Path

try:
    import openai
except ImportError:
    print("ERROR: run: pip install openai"); sys.exit(1)

try:
    import tiktoken
except ImportError:
    print("ERROR: run: pip install tiktoken"); sys.exit(1)

CATALOG     = Path(__file__).parent / "pdfs.json"
PDFS_DIR    = Path(__file__).parent / "pdfs"
MD_DIR      = Path(__file__).parent / "markdown"
RESULTS_DIR = Path(__file__).parent / "results"

DUMMY_Q = "What is the main topic of this document?"
MODEL   = "gpt-4o-mini"


def count_pdf_tokens(client: openai.OpenAI, pdf_path: Path) -> int:
    with open(pdf_path, "rb") as f:
        uploaded = client.files.create(file=f, purpose="user_data")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            max_tokens=1,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": uploaded.id}},
                    {"type": "text", "text": DUMMY_Q},
                ],
            }],
        )
        return resp.usage.prompt_tokens
    finally:
        client.files.delete(uploaded.id)


def count_text_tokens_local(text: str) -> int:
    try:
        enc = tiktoken.encoding_for_model(MODEL)
    except KeyError:
        enc = tiktoken.get_encoding("o200k_base")
    wrapped = f"<document>\n{text}\n</document>\n\n{DUMMY_Q}"
    return len(enc.encode(wrapped))


def read_text(pdf_stem: str, tool: str, suffix: str = ".md") -> str | None:
    path = MD_DIR / tool / (pdf_stem + suffix)
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else None


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        print("Get one at: https://platform.openai.com/api-keys")
        sys.exit(1)

    client  = openai.OpenAI(api_key=api_key)
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(exist_ok=True)

    results_file = RESULTS_DIR / "tokens_openai.json"
    results = json.loads(results_file.read_text()) if results_file.exists() else {}

    for entry in catalog:
        pdf_id   = entry["id"]
        pdf_stem = entry["filename"].replace(".pdf", "")
        pdf_path = PDFS_DIR / entry["filename"]
        rec      = results.get(pdf_id, {})
        changed  = False

        if not pdf_path.exists():
            print(f"SKIP {entry['name'][:40]}: not downloaded"); continue

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
            time.sleep(1)

        for tool, suffix in [("pymupdf4llm", ".md"), ("pdftotext", ".txt")]:
            if tool not in rec:
                text = read_text(pdf_stem, tool, suffix)
                if text:
                    print(f"    counting {tool} (tiktoken, local)…", end=" ", flush=True)
                    rec[tool] = count_text_tokens_local(text)
                    changed = True
                    print(f"{rec[tool]:,}")

        rec["name"] = entry["name"]
        rec["type"] = entry["type"]
        results[pdf_id] = rec
        if changed:
            results_file.write_text(json.dumps(results, indent=2))

    # ── three-way comparison table ────────────────────────────────────────────
    anthropic = json.loads((RESULTS_DIR / "tokens.json").read_text())         if (RESULTS_DIR / "tokens.json").exists()         else {}
    gemini    = json.loads((RESULTS_DIR / "tokens_gemini.json").read_text())  if (RESULTS_DIR / "tokens_gemini.json").exists()  else {}

    w = 34
    print(f"\n\n{'Document':<{w}} {'── Anthropic ──':^20} {'── Gemini ──':^20} {'── OpenAI ──':^20}")
    print(f"{'':^{w}} {'raw PDF':>9} {'ratio':>7}   {'raw PDF':>9} {'ratio':>7}   {'raw PDF':>9} {'ratio':>7}")
    print("─" * 110)

    for entry in catalog:
        pid   = entry["id"]
        a, g, o = anthropic.get(pid, {}), gemini.get(pid, {}), results.get(pid, {})

        # ratio = raw_pdf / that provider's own markdown count
        a_raw = a.get("raw_pdf"); a_md = a.get("pymupdf4llm")
        g_raw = g.get("raw_pdf"); g_md = g.get("pymupdf4llm")
        o_raw = o.get("raw_pdf"); o_md = o.get("pymupdf4llm")

        a_r = f"{a_raw/a_md:.0%}" if a_raw and a_md else "—"
        g_r = f"{g_raw/g_md:.0%}" if g_raw and g_md else "—"
        o_r = f"{o_raw/o_md:.0%}" if o_raw and o_md else "—"

        print(
            f"  {entry['name'][:w-2]:<{w-2}}"
            f"  {f'{a_raw:,}' if a_raw else '—':>9} {a_r:>7}"
            f"   {f'{g_raw:,}' if g_raw else '—':>9} {g_r:>7}"
            f"   {f'{o_raw:,}' if o_raw else '—':>9} {o_r:>7}"
        )

    print("\nratio = raw PDF tokens / markdown tokens for the same provider")
    print("<100% means raw PDF is cheaper than markdown (Gemini pattern)")
    print(">100% means raw PDF costs more than markdown (Anthropic pattern)")
    print(f"\nOpenAI results saved to {results_file}")


if __name__ == "__main__":
    main()
