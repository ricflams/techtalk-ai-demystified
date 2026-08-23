<#
.SYNOPSIS
    Build the readable (non-slideshow) page locally and open it in a browser.

.DESCRIPTION
    Renders src/slides.md to public/index.html via make_readable.py and syncs
    the images it references. This is the same output the GitHub Pages build
    publishes as the site's front page -- it does NOT build the slideshow
    (that needs the Marp CLI; see CLAUDE.md).

    The page is plain static HTML with relative image paths, so it opens
    straight from disk -- no local web server needed.

.PARAMETER Watch
    Stay running and rebuild whenever slides.md or make_readable.py changes.
    Refresh the browser tab (F5) to see each rebuild.

.PARAMETER NoOpen
    Build only; don't launch a browser.

.EXAMPLE
    scripts\build-readable.ps1
    Build once and open it.

.EXAMPLE
    scripts\build-readable.ps1 -Watch
    Rebuild on every save while you edit.
#>
[CmdletBinding()]
param(
    [switch]$Watch,
    [switch]$NoOpen
)

$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$slides = 'src\slides.md'
$script = 'scripts\make_readable.py'
$output = 'public\index.html'

function Invoke-Build {
    New-Item -ItemType Directory -Force -Path 'public' | Out-Null

    # robocopy mirrors incrementally -- a full copy of ~260 images takes about
    # 1.8s every run, this takes ~0.07s once they're in place. Exit codes
    # below 8 are success (1 = files copied, 2 = extras removed, 3 = both);
    # only 8+ is an actual failure.
    robocopy 'src\images' 'public\images' /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed syncing images (exit $LASTEXITCODE)" }
    $global:LASTEXITCODE = 0

    python $script $slides $output
    if ($LASTEXITCODE -ne 0) {
        throw "make_readable.py failed (exit $LASTEXITCODE). If it can't import 'markdown', run: pip install markdown"
    }
}

Invoke-Build
$full = (Resolve-Path $output).Path
Write-Host "Built $full" -ForegroundColor Green

if (-not $NoOpen) { Start-Process $full }

if (-not $Watch) { return }

Write-Host "Watching $slides -- press Ctrl-C to stop. Refresh the browser (F5) after each rebuild." -ForegroundColor Cyan

# Polled rather than FileSystemWatcher: editors commonly save via a temp file
# plus rename, which fires a confusing burst of events; comparing timestamps
# is simpler and misses nothing that matters at this cadence.
function Get-Stamp {
    (Get-Item $slides, $script | ForEach-Object { $_.LastWriteTimeUtc.Ticks }) -join ','
}

$last = Get-Stamp
while ($true) {
    Start-Sleep -Milliseconds 500
    $now = Get-Stamp
    if ($now -eq $last) { continue }
    $last = $now
    try {
        Invoke-Build
        Write-Host ("[{0}] rebuilt" -f (Get-Date -Format 'HH:mm:ss')) -ForegroundColor Green
    }
    catch {
        Write-Host ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $_.Exception.Message) -ForegroundColor Red
    }
}
