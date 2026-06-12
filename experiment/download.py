#!/usr/bin/env python3
"""Download the 10 experiment PDFs."""
import json
import subprocess
import sys
from pathlib import Path

PDFS_DIR = Path(__file__).parent / "pdfs"
CATALOG = Path(__file__).parent / "pdfs.json"

HEADERS = [
    "--user-agent", "Mozilla/5.0 (compatible; research-experiment/1.0)",
    "--timeout", "60",
    "--tries", "3",
    "-4",   # force IPv4 — WSL2 often has broken IPv6
]


def download(entry: dict) -> bool:
    dest = PDFS_DIR / entry["filename"]
    if dest.exists() and dest.stat().st_size > 10_000:
        size_kb = dest.stat().st_size // 1024
        print(f"  SKIP  {entry['filename']} (already {size_kb} KB)")
        return True

    print(f"  GET   {entry['filename']}  ← {entry['url']}")
    cmd = ["wget", *HEADERS, "-O", str(dest), entry["url"]]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0 or not dest.exists() or dest.stat().st_size < 1000:
        print(f"  FAIL  {entry['filename']}: {result.stderr.decode()[-200:]}")
        dest.unlink(missing_ok=True)
        return False

    size_kb = dest.stat().st_size // 1024
    print(f"  OK    {entry['filename']} ({size_kb} KB)")
    return True


def main():
    PDFS_DIR.mkdir(exist_ok=True)
    catalog = json.loads(CATALOG.read_text())

    print(f"Downloading {len(catalog)} PDFs to {PDFS_DIR}/\n")
    ok = failed = 0
    for entry in catalog:
        if download(entry):
            ok += 1
        else:
            failed += 1

    print(f"\nDone: {ok} OK, {failed} failed.")
    if failed:
        print("Failed downloads can be retried by re-running this script.")
        sys.exit(1)


if __name__ == "__main__":
    main()
