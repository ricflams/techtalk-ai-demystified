#!/usr/bin/env python3
"""
Two verification tests for the Gemini raw-PDF token finding:

  Test 1 — count_tokens vs actual usage
    Make a real inference call for each PDF and compare the predicted token count
    (from measure_tokens_gemini.py) against response.usage_metadata.prompt_token_count.
    If they match, the count_tokens measurement is reliable.

  Test 2 — end-of-document questions
    Ask 2 questions that can only be answered from content near the END of each document.
    Run each question with both raw PDF and pymupdf4llm markdown.
    If raw PDF gives coherent answers matching markdown, extraction is complete.
    If raw PDF gives vague/wrong answers, content is being truncated or lost.

Results saved to results/verify_gemini.json
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
    print("ERROR: run: pip install google-genai"); sys.exit(1)

CATALOG     = Path(__file__).parent / "pdfs.json"
PDFS_DIR    = Path(__file__).parent / "pdfs"
MD_DIR      = Path(__file__).parent / "markdown" / "pymupdf4llm"
RESULTS_DIR = Path(__file__).parent / "results"

MODEL = "gemini-2.5-flash"

# Questions that reference content near the END or deep within each document.
# A model with truncated/incomplete access should struggle with these.
END_QUESTIONS = {
    "attention": [
        "What future research directions beyond text do the authors suggest in the conclusion?",
        "In the English constituency parsing experiments, what was the WSJ training set size used for fine-tuning?",
    ],
    "resnet": [
        "What detection method was used when applying ResNets to PASCAL VOC and MS COCO, and what mAP did it achieve?",
        "The 1202-layer network got a worse result than the 110-layer network — what explanation do the authors give?",
    ],
    "gpt3": [
        "What does the data contamination analysis in Appendix C find for the TriviaQA benchmark?",
        "What few-shot BLEU score does GPT-3 175B achieve on the French-to-English WMT14 translation task?",
    ],
    "irs1040": [
        "What exactly does the 'Third Party Designee' section at the bottom of the form ask for?",
        "What is the form number and tax year printed at the very bottom footer of the form?",
    ],
    "nist_cloud": [
        "What are the full names of both authors listed on the document?",
        "What does the document say in its final note about the definition being a 'working definition'?",
    ],
    "nist_csf": [
        "How does Appendix A describe the relationship between the Framework and the Baldrige Cybersecurity Excellence Builder?",
        "How is 'Risk' defined in the Glossary at the end of the document?",
    ],
    "bert": [
        "What does Table 6 in the ablation study show about the number of training steps needed for BERT?",
        "In the conclusion, what does the paper identify as the most important contribution?",
    ],
    "word2vec": [
        "What accuracy does the best model achieve on the semantic word relationship test questions specifically?",
        "What does the conclusion identify as the main advantage of the proposed models over RNN language models?",
    ],
    "clip": [
        "What specific concern about facial recognition or surveillance does the Broader Impacts section raise?",
        "In Appendix D, what does the analysis of natural distribution shift robustness show about CLIP vs ImageNet models?",
    ],
    "gans": [
        "What Parzen window log-likelihood value is reported for MNIST, and how does it compare to prior work?",
        "In the Advantages and disadvantages section, what specific disadvantage of GANs is mentioned regarding Pg(x)?",
    ],
}


def upload_pdf(client, pdf_path: Path):
    uploaded = client.files.upload(
        file=str(pdf_path),
        config=types.UploadFileConfig(mime_type="application/pdf"),
    )
    for _ in range(30):
        f = client.files.get(name=uploaded.name)
        if str(f.state).endswith("ACTIVE"):
            return uploaded
        time.sleep(2)
    raise TimeoutError(f"File {pdf_path.name} never became ACTIVE")


def ask(client, contents, max_tokens=512) -> tuple[str, int]:
    for attempt in range(5):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(max_output_tokens=max_tokens),
            )
            tokens = resp.usage_metadata.prompt_token_count
            text   = resp.text if resp.text else "(no response)"
            return text, tokens
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt < 4:
                wait = 60 * (attempt + 1)
                print(f"rate limited — waiting {wait}s…", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)

    client  = genai.Client(api_key=api_key)
    catalog = json.loads(CATALOG.read_text())
    RESULTS_DIR.mkdir(exist_ok=True)

    out_file = RESULTS_DIR / "verify_gemini.json"
    results  = json.loads(out_file.read_text()) if out_file.exists() else {}

    prev_counts = {}
    tokens_file = RESULTS_DIR / "tokens_gemini.json"
    if tokens_file.exists():
        prev_counts = json.loads(tokens_file.read_text())

    for entry in catalog:
        pdf_id   = entry["id"]
        pdf_path = PDFS_DIR / entry["filename"]
        md_path  = MD_DIR / entry["filename"].replace(".pdf", ".md")
        rec      = results.get(pdf_id, {})

        if not pdf_path.exists():
            print(f"\nSKIP {pdf_id}: not downloaded"); continue

        print(f"\n{'='*60}")
        print(f"  {entry['name']}")
        print(f"{'='*60}")

        # ── Test 1: verify count_tokens prediction ────────────────────────────
        if "token_verification" not in rec or "error" in rec.get("token_verification", {}):
            print(f"  [Test 1] uploading PDF for real inference call…")
            try:
                uploaded = upload_pdf(client, pdf_path)
                _, actual = ask(client, [uploaded, "What is the main topic?"])
                client.files.delete(name=uploaded.name)

                predicted = prev_counts.get(pdf_id, {}).get("raw_pdf")
                rec["token_verification"] = {
                    "predicted": predicted,
                    "actual":    actual,
                    "match":     abs(actual - predicted) / predicted < 0.05 if predicted else None,
                }
                print(f"  [Test 1] predicted={predicted:,}  actual={actual:,}  "
                      f"delta={abs(actual-predicted)/predicted:.1%}" if predicted else
                      f"  [Test 1] actual={actual:,}  (no prediction to compare)")
            except Exception as e:
                print(f"  [Test 1] ERROR: {e}")
                rec["token_verification"] = {"error": str(e)}

            results[pdf_id] = rec
            out_file.write_text(json.dumps(results, indent=2))
            time.sleep(1)

        else:
            v = rec["token_verification"]
            print(f"  [Test 1] SKIP — predicted={v.get('predicted')}, actual={v.get('actual')}")

        # ── Test 2: end-of-document questions ─────────────────────────────────
        questions = END_QUESTIONS.get(pdf_id, [])
        md_text   = md_path.read_text(encoding="utf-8", errors="replace") if md_path.exists() else None

        for i, question in enumerate(questions, 1):
            key = f"q{i}"
            if key in rec.get("end_questions", {}) and "error" not in rec["end_questions"][key].get("pdf", {}):
                print(f"  [Test 2 Q{i}] SKIP"); continue

            print(f"\n  [Test 2 Q{i}] {question[:70]}")

            q_rec = {}

            # raw PDF
            print(f"    raw PDF…", end=" ", flush=True)
            try:
                uploaded = upload_pdf(client, pdf_path)
                answer, tokens = ask(client, [uploaded, question])
                client.files.delete(name=uploaded.name)
                q_rec["pdf"] = {"answer": answer, "tokens": tokens}
                print(f"({tokens:,} tokens) → {answer[:80].replace(chr(10), ' ')}")
            except Exception as e:
                print(f"ERROR: {e}")
                q_rec["pdf"] = {"error": str(e)}
            time.sleep(1)

            # markdown
            if md_text:
                print(f"    markdown…", end=" ", flush=True)
                try:
                    prompt = f"<document>\n{md_text}\n</document>\n\n{question}"
                    answer, tokens = ask(client, prompt)
                    q_rec["markdown"] = {"answer": answer, "tokens": tokens}
                    print(f"({tokens:,} tokens) → {answer[:80].replace(chr(10), ' ')}")
                except Exception as e:
                    print(f"ERROR: {e}")
                    q_rec["markdown"] = {"error": str(e)}
                time.sleep(1)

            if "end_questions" not in rec:
                rec["end_questions"] = {}
            rec["end_questions"][key] = {"question": question, **q_rec}
            results[pdf_id] = rec
            out_file.write_text(json.dumps(results, indent=2))

    # ── summary ───────────────────────────────────────────────────────────────
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    print(f"\n[Test 1] count_tokens accuracy:")
    print(f"  {'Document':<40} {'Predicted':>10} {'Actual':>10} {'Delta':>8} {'OK?':>5}")
    for entry in catalog:
        pid = entry["id"]
        v   = results.get(pid, {}).get("token_verification", {})
        if "error" in v or not v:
            continue
        p, a = v.get("predicted"), v.get("actual")
        if p and a:
            delta = (a - p) / p
            ok = "✓" if abs(delta) < 0.10 else "✗"
            print(f"  {entry['name'][:40]:<40} {p:>10,} {a:>10,} {delta:>+7.1%} {ok:>5}")

    print(f"\n[Test 2] End-of-document answer quality (first answer per PDF):")
    for entry in catalog:
        pid = entry["id"]
        eqs = results.get(pid, {}).get("end_questions", {})
        if not eqs:
            continue
        print(f"\n  {entry['name']}")
        for qkey, qdata in eqs.items():
            print(f"    Q: {qdata['question'][:70]}")
            pdf_ans = qdata.get("pdf", {}).get("answer", "—")
            md_ans  = qdata.get("markdown", {}).get("answer", "—")
            print(f"    PDF: {pdf_ans[:120].replace(chr(10), ' ')}")
            print(f"    MD:  {md_ans[:120].replace(chr(10), ' ')}")

    print(f"\nFull results: {out_file}")


if __name__ == "__main__":
    main()
