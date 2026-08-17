#!/usr/bin/env python3
"""
Convert PDFs to markdown using multiple tools for comparison.

Converters tried (best → baseline):
  1. marker-pdf   — ML-based, handles math/tables/images best (needs: pip install marker-pdf)
  2. pymupdf4llm  — lightweight, solid markdown output (needs: pip install pymupdf4llm)
  3. pdftotext    — plain text, no formatting (needs: apt install poppler-utils)
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

CATALOG = Path(__file__).parent / "pdfs.json"
PDFS_DIR = Path(__file__).parent / "pdfs"
MD_DIR = Path(__file__).parent / "markdown"


# ── pdftotext ──────────────────────────────────────────────────────────────────

def convert_pdftotext(pdf: Path, out_dir: Path) -> Path | None:
    if not shutil.which("pdftotext"):
        print("    pdftotext not found (run: sudo apt install poppler-utils)")
        return None
    dest = out_dir / (pdf.stem + ".txt")
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(dest)],
        capture_output=True,
    )
    if result.returncode != 0 or not dest.exists():
        print(f"    pdftotext failed: {result.stderr.decode()[:200]}")
        return None
    return dest


# ── pymupdf4llm ────────────────────────────────────────────────────────────────

def convert_pymupdf4llm(pdf: Path, out_dir: Path) -> Path | None:
    try:
        import pymupdf4llm
    except ImportError:
        print("    pymupdf4llm not found (run: pip install pymupdf4llm)")
        return None
    dest = out_dir / (pdf.stem + ".md")
    try:
        md = pymupdf4llm.to_markdown(str(pdf))
        dest.write_text(md, encoding="utf-8")
        return dest
    except Exception as e:
        print(f"    pymupdf4llm failed: {e}")
        return None


# ── marker ─────────────────────────────────────────────────────────────────────
# marker-pdf's API changed between v0.x and v1.x. This targets v1.x
# (marker.converters.pdf.PdfConverter / marker.models.create_model_dict), which is
# what `pip install marker-pdf` currently installs. The model dict is loaded once
# and reused across PDFs since that's the slow part (downloads + GPU/CPU load).

_marker_converter = None


def _get_marker_converter():
    global _marker_converter
    if _marker_converter is None:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        # This machine's GPU is a 4GB T400 shared with the desktop session — marker's
        # 5-model pipeline OOMs on it. Force CPU; slower, but this only needs to run once.
        print("    loading marker models on CPU (slow first time, downloads weights)…")
        _marker_converter = PdfConverter(artifact_dict=create_model_dict(device="cpu"))
    return _marker_converter


def convert_marker(pdf: Path, out_dir: Path) -> Path | None:
    try:
        from marker.output import text_from_rendered
    except ImportError:
        print("    marker not installed (optional: pip install marker-pdf)")
        return None

    dest = out_dir / (pdf.stem + ".md")
    try:
        converter = _get_marker_converter()
        rendered = converter(str(pdf))
        text, _ext, _images = text_from_rendered(rendered)
        dest.write_text(text, encoding="utf-8")
        return dest
    except Exception as e:
        print(f"    marker failed: {e}")
        return None


# ── main ───────────────────────────────────────────────────────────────────────

def convert_one(entry: dict) -> dict:
    pdf = PDFS_DIR / entry["filename"]
    if not pdf.exists():
        print(f"  SKIP  {entry['filename']} not downloaded yet")
        return {}

    results = {"id": entry["id"]}

    print(f"\n  {entry['name']} ({pdf.stat().st_size // 1024} KB)")

    for tool, func, subdir in [
        ("pdftotext",   convert_pdftotext,   "pdftotext"),
        ("pymupdf4llm", convert_pymupdf4llm, "pymupdf4llm"),
        ("marker",      convert_marker,      "marker"),
    ]:
        out_dir = MD_DIR / subdir
        out_dir.mkdir(parents=True, exist_ok=True)

        dest_check = out_dir / (pdf.stem + ".md")
        txt_check  = out_dir / (pdf.stem + ".txt")
        if dest_check.exists() or txt_check.exists():
            existing = dest_check if dest_check.exists() else txt_check
            size_kb = existing.stat().st_size // 1024
            print(f"    SKIP  {tool} (already {size_kb} KB)")
            results[tool] = str(existing)
            continue

        print(f"    RUN   {tool}…", end=" ", flush=True)
        dest = func(pdf, out_dir)
        if dest:
            size_kb = dest.stat().st_size // 1024
            print(f"→ {size_kb} KB")
            results[tool] = str(dest)
        else:
            print("→ skipped")

    return results


def main():
    catalog = json.loads(CATALOG.read_text())
    print(f"Converting {len(catalog)} PDFs using pdftotext / pymupdf4llm / marker\n")

    for entry in catalog:
        convert_one(entry)

    print("\nDone. Markdown files in markdown/")


if __name__ == "__main__":
    main()
