#!/usr/bin/env python3
"""
Verify the Claude raw-PDF token finding — the one thing measure_tokens.py never checked.

Unlike Gemini (verified in verify_gemini.py — count_tokens matched real usage to <0.1%)
and OpenAI (whose raw-PDF number was already a real inference call, not an estimate),
Claude's raw_pdf figure in results/tokens.json came ONLY from the free count_tokens()
dry-run endpoint. It was never cross-checked against what a real messages.create() call
actually bills. This makes one real inference call per PDF (same dummy question
measure_tokens.py used, so the comparison is apples-to-apples) and compares the real
billed input tokens against the count_tokens prediction.

Results saved to results/verify_claude.json
"""
import base64
import json
import os
import sys
import time
from pathlib import Path

import anthropic

CATALOG     = Path(__file__).parent / "pdfs.json"
PDFS_DIR    = Path(__file__).parent / "pdfs"
RESULTS_DIR = Path(__file__).parent / "results"
TOKENS_FILE = RESULTS_DIR / "tokens.json"
OUT_FILE    = RESULTS_DIR / "verify_claude.json"

MODEL = "claude-haiku-4-5-20251001"  # match measure_tokens.py's model choice exactly
DUMMY_Q = "What is the main topic of this document?"  # same question measure_tokens.py used


def extract_text(resp) -> str:
    for block in resp.content:
        if block.type == "text":
            return block.text
    return "(no text block)"


def real_pdf_tokens(client, pdf_path: Path) -> tuple[int, str]:
    data = base64.standard_b64encode(pdf_path.read_bytes()).decode()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=100,
        thinking={"type": "disabled"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}},
                {"type": "text", "text": DUMMY_Q},
            ],
        }],
    )
    return resp.usage.input_tokens, extract_text(resp)


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set"); sys.exit(1)

    client  = anthropic.Anthropic()
    catalog = json.loads(CATALOG.read_text())
    predicted_counts = json.loads(TOKENS_FILE.read_text()) if TOKENS_FILE.exists() else {}
    results = json.loads(OUT_FILE.read_text()) if OUT_FILE.exists() else {}

    print(f"Model: {MODEL}  (matches measure_tokens.py's model choice)\n")

    for entry in catalog:
        pdf_id = entry["id"]
        pdf_path = PDFS_DIR / entry["filename"]

        if not pdf_path.exists():
            print(f"SKIP {pdf_id}: not downloaded"); continue
        if pdf_id in results and "error" not in results[pdf_id]:
            print(f"SKIP {pdf_id}: already verified"); continue

        predicted = predicted_counts.get(pdf_id, {}).get("raw_pdf")
        print(f"{entry['name']:50}", end=" ", flush=True)

        try:
            actual, sample_answer = real_pdf_tokens(client, pdf_path)
            delta = (actual - predicted) / predicted if predicted else None
            results[pdf_id] = {
                "predicted": predicted,
                "actual":    actual,
                "delta_pct": round(delta * 100, 2) if delta is not None else None,
                "match_5pct": abs(delta) < 0.05 if delta is not None else None,
            }
            print(f"predicted={predicted:,}  actual={actual:,}  delta={delta:+.1%}" if delta is not None
                  else f"actual={actual:,}  (no prediction on file)")
            OUT_FILE.write_text(json.dumps(results, indent=2))
            time.sleep(0.5)
        except anthropic.RateLimitError:
            print("rate limited — waiting 30s…")
            time.sleep(30)
        except Exception as e:
            print(f"ERROR: {e}")
            results[pdf_id] = {"error": str(e)}
            OUT_FILE.write_text(json.dumps(results, indent=2))

    print(f"\nWritten to {OUT_FILE}")
    deltas = [v["delta_pct"] for v in results.values() if v.get("delta_pct") is not None]
    if deltas:
        avg = sum(deltas) / len(deltas)
        print(f"Average delta across {len(deltas)} docs: {avg:+.1f}%  "
              f"(positive = real inference billed MORE than count_tokens predicted)")


if __name__ == "__main__":
    main()
