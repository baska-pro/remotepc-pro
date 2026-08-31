# Installation

## Recommended installation

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

It creates a Python virtual environment and installs the dependencies from `requirements.txt`. It does **not** create a Scheduled Task, service, or hidden startup entry.

## Configure

Edit:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Set at least `bot_token` and `allowed_chat_ids`, then run:

```powershell
%LOCALAPPDATA%\Programs\RemotePCPro\.venv\Scripts\python.exe `
  %LOCALAPPDATA%\Programs\RemotePCPro\remotepc_pro.py
```

The dashboard listens on `127.0.0.1:8765` by default.
