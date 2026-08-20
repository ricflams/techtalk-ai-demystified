# Open the live slideshow (to share/present) and the speaker-notes page
# (to keep on your own screen) as two separate browser windows, synced
# live via BroadcastChannel as you navigate slides.
#
# Usage: scripts\present.ps1

$base = "https://ricflams.github.io/techtalk-ai-demystified"

Start-Process "$base/presentation.html"
Start-Process "$base/notes.html"

Write-Host "Share/fullscreen the 'presentation.html' window; keep 'notes.html' private on your own screen."
