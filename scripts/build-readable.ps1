# Rebuild the readable (non-slideshow) page for local preview.
# Usage: scripts\build-readable.ps1
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\.."

Remove-Item -Recurse -Force public\images -ErrorAction SilentlyContinue
Copy-Item -Recurse src\images public\images
python scripts\make_readable.py src\slides.md public\index.html

Write-Host "Open public\index.html directly in a browser to preview."
