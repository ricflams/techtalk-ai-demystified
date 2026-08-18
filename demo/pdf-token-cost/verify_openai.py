#!/usr/bin/env python3
"""
Verify the OpenAI raw-PDF finding — the one leg of the token-cost comparison that was
never checked beyond aggregate token-count parity.

measure_tokens_openai.py measures raw PDF with a real inference call (trustworthy by
construction) but markdown with a local tiktoken simulation (never verified against a
real call), and never tested WHAT the "file" content type actually does with a PDF —
pure server-side text extraction (as findings.md assumes), or a text+vision hybrid.

Three checks:
  1. Markdown token count: local tiktoken estimate vs. a real chat.completions call,
     for both pdftotext and pymupdf4llm output. Tests the asymmetric-methodology concern.
  2. End-of-document questions on the 3 largest PDFs (gpt3, clip, nist_csf) via raw PDF —
     same questions verify_gemini.py used, for direct comparability. Tests truncation.
  3. A figure/diagram question via raw PDF on a visually-rich document (attention's
     architecture diagram, CLIP's example images) — tests whether images are processed
     at all, or if it's text-only.

Results saved to results/verify_openai.json
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
OUT_FILE    = RESULTS_DIR / "verify_openai.json"

MODEL = "gpt-4o-mini"  # match measure_tokens_openai.py's model choice

END_QUESTIONS = {
    "gpt3": [
        "What does the data contamination analysis in Appendix C find for the TriviaQA benchmark?",
        "What few-shot BLEU score does GPT-3 175B achieve on the French-to-English WMT14 translation task?",
    ],
    "clip": [
        "What specific concern about facial recognition or surveillance does the Broader Impacts section raise?",
        "In Appendix D, what does the analysis of natural distribution shift robustness show about CLIP vs ImageNet models?",
    ],
    "nist_csf": [
        "How does Appendix A describe the relationship between the Framework and the Baldrige Cybersecurity Excellence Builder?",
        "How is 'Risk' defined in the Glossary at the end of the document?",
    ],
}

FIGURE_QUESTIONS = {
    "attention": "Describe exactly what the architecture diagram in Figure 1 shows — the boxes, "
                 "their labels, and how they're connected. This is only answerable by seeing the "
                 "actual diagram image, not by reading surrounding text.",
    "clip": "The paper includes a Figure 1 schematic with three numbered steps (1) Contrastive "
            "pre-training, (2) Create dataset classifier from label text, (3) Use for zero-shot "
            "prediction. Describe what the actual diagram/icons show for each of these three "
            "steps, not just the caption text.",
}


def upload_and_ask(client, pdf_path: Path, question: str, max_tokens=500) -> tuple[str, dict]:
    with open(pdf_path, "rb") as f:
        uploaded = client.files.create(file=f, purpose="user_data")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": uploaded.id}},
                    {"type": "text", "text": question},
                ],
            }],
        )
        answer = resp.choices[0].message.content
        usage = {"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens}
        return answer, usage
    finally:
        client.files.delete(uploaded.id)


def ask_text(client, text: str, question: str, max_tokens=10) -> int:
    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": f"<document>\n{text}\n</document>\n\n{question}"}],
    )
    return resp.usage.prompt_tokens


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set"); sys.exit(1)

    client = openai.OpenAI(api_key=api_key)
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(exist_ok=True)
    results = json.loads(OUT_FILE.read_text()) if OUT_FILE.exists() else {}

    DUMMY_Q = "What is the main topic of this document?"

    # ── Test 1: markdown token count, local tiktoken vs real call ──────────────
    print("=== Test 1: markdown token count — tiktoken estimate vs real call ===")
    results.setdefault("markdown_verification", {})
    for entry in catalog:
        pid = entry["id"]
        stem = entry["filename"].replace(".pdf", "")
        if pid in results["markdown_verification"]:
            continue
        md_path = MD_DIR / "pymupdf4llm" / f"{stem}.md"
        if not md_path.exists():
            continue
        text = md_path.read_text(encoding="utf-8", errors="replace")
        try:
            enc = tiktoken.encoding_for_model(MODEL)
        except KeyError:
            enc = tiktoken.get_encoding("o200k_base")
        wrapped = f"<document>\n{text}\n</document>\n\n{DUMMY_Q}"
        predicted = len(enc.encode(wrapped))
        actual = ask_text(client, text, DUMMY_Q)
        delta = (actual - predicted) / predicted
        results["markdown_verification"][pid] = {"predicted": predicted, "actual": actual, "delta_pct": round(delta * 100, 2)}
        print(f"  {entry['name'][:45]:45} predicted={predicted:,}  actual={actual:,}  delta={delta:+.1%}")
        OUT_FILE.write_text(json.dumps(results, indent=2))
        time.sleep(0.5)

    # ── Test 2: end-of-document questions (truncation check) ───────────────────
    print("\n=== Test 2: end-of-document questions (raw PDF) ===")
    results.setdefault("end_questions", {})
    for pid, questions in END_QUESTIONS.items():
        if pid in results["end_questions"]:
            print(f"  SKIP {pid}: already done"); continue
        pdf_path = PDFS_DIR / f"{pid}.pdf"
        print(f"  --- {pid} ---")
        answers = []
        for q in questions:
            try:
                answer, usage = upload_and_ask(client, pdf_path, q)
                print(f"  Q: {q}")
                print(f"  A: {answer[:500]}")
                print(f"     [prompt_tokens={usage['prompt_tokens']:,}]\n")
                answers.append({"question": q, "answer": answer, "usage": usage})
            except Exception as e:
                print(f"  ERROR: {e}")
                answers.append({"question": q, "error": str(e)})
            time.sleep(1)
        results["end_questions"][pid] = answers
        OUT_FILE.write_text(json.dumps(results, indent=2))

    # ── Test 3: figure/diagram comprehension (vision-vs-text-only check) ───────
    print("\n=== Test 3: figure/diagram comprehension (raw PDF) ===")
    results.setdefault("figure_questions", {})
    for pid, question in FIGURE_QUESTIONS.items():
        if pid in results["figure_questions"]:
            print(f"  SKIP {pid}: already done"); continue
        pdf_path = PDFS_DIR / f"{pid}.pdf"
        print(f"  --- {pid} ---")
        try:
            answer, usage = upload_and_ask(client, pdf_path, question, max_tokens=600)
            print(f"  Q: {question}")
            print(f"  A: {answer}")
            print(f"     [prompt_tokens={usage['prompt_tokens']:,}]\n")
            results["figure_questions"][pid] = {"question": question, "answer": answer, "usage": usage}
        except Exception as e:
            print(f"  ERROR: {e}")
            results["figure_questions"][pid] = {"question": question, "error": str(e)}
        OUT_FILE.write_text(json.dumps(results, indent=2))
        time.sleep(1)

    print(f"\nWritten to {OUT_FILE}")


if __name__ == "__main__":
    main()
