param(
    [switch]$RemoveData
)

$ErrorActionPreference = "Stop"
$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\RemotePCPro"
$StateDir = Join-Path $env:LOCALAPPDATA "RemotePCPro"

if (Test-Path $InstallDir) {
    Remove-Item -Recurse -Force $InstallDir
    Write-Host "Removed application files: $InstallDir"
}

if ($RemoveData -and (Test-Path $StateDir)) {
    Remove-Item -Recurse -Force $StateDir
    Write-Host "Removed runtime data: $StateDir"
} else {
    Write-Host "Runtime data kept: $StateDir"
}

Write-Host "If you manually created a Scheduled Task, remove it separately."
