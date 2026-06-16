#!/bin/bash
set -e

echo "=== PDF Experiment Setup ==="

# System deps
echo ""
echo "--- Installing system packages ---"
sudo apt-get update -q
sudo apt-get install -y poppler-utils wget

# Python deps
echo ""
echo "--- Installing Python packages ---"
pip install --upgrade anthropic pymupdf4llm rich

# Optional: marker-pdf (best quality, ~2GB models, GPU helps but not required)
echo ""
echo "--- Optional: marker-pdf (ML-based, best quality) ---"
read -rp "Install marker-pdf? It downloads ~2GB of models. [y/N] " ans
if [[ "$ans" =~ ^[Yy]$ ]]; then
    pip install marker-pdf
    echo "marker-pdf installed."
else
    echo "Skipping marker-pdf. pymupdf4llm will be used as primary converter."
fi

# Create directories
mkdir -p pdfs markdown/pdftotext markdown/pymupdf4llm markdown/marker results/answers

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Set your Anthropic API key:"
echo "  export ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "Then run the experiment:"
echo "  python download.py          # Download all 10 PDFs"
echo "  python convert.py           # Convert to markdown"
echo "  python measure_tokens.py    # Count tokens (free API call)"
echo "  python run_qa.py            # Run QA experiment (costs ~\$3-5)"
echo "  python report.py            # Generate report"
