$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\RemotePCPro"
$StateDir = Join-Path $env:LOCALAPPDATA "RemotePCPro"
$VenvDir = Join-Path $InstallDir ".venv"

Write-Host "Installing RemotePC Pro to $InstallDir"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path $StateDir | Out-Null

$files = @(
    "remotepc_pro.py",
    "requirements.txt",
    "VERSION",
    "LICENSE"
)
foreach ($file in $files) {
    Copy-Item -Force (Join-Path $ProjectRoot $file) (Join-Path $InstallDir $file)
}

$SourceDir = Join-Path $ProjectRoot "src"
$InstalledSourceDir = Join-Path $InstallDir "src"
if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
    throw "Source directory missing: $SourceDir"
}
if (Test-Path -LiteralPath $InstalledSourceDir) {
    Remove-Item -Recurse -Force $InstalledSourceDir
}
Copy-Item -Recurse -Force $SourceDir $InstalledSourceDir

$ConfigPath = Join-Path $StateDir "RemotePC.config.json"
if (-not (Test-Path $ConfigPath)) {
    Copy-Item (Join-Path $ProjectRoot "RemotePC.config.example.json") $ConfigPath
}

$Python = Get-Command python -ErrorAction Stop
& $Python.Source -m venv $VenvDir
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
& $VenvPython -m pip install --disable-pip-version-check --upgrade pip
& $VenvPython -m pip install --disable-pip-version-check -r (Join-Path $InstallDir "requirements.txt")

Write-Host ""
Write-Host "Installed."
Write-Host "Config: $ConfigPath"
Write-Host "Edit the config before starting RemotePC Pro."
Write-Host "No Scheduled Task or hidden startup entry was created."
