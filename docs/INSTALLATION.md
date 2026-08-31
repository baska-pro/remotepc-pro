# Installation

## Recommended

Open PowerShell as the Windows user that will run RemotePC Pro:

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer creates:

```text
%LOCALAPPDATA%\Programs\RemotePCPro
%LOCALAPPDATA%\RemotePCPro
```

It does not silently create a Scheduled Task.

After installation, edit:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Then launch the application from PowerShell or a shortcut you create yourself.

## Optional dependencies

FFmpeg and NirCmd are not bundled. Install them separately and configure their paths if you intentionally use features that depend on them.
