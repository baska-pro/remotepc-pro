# RemotePC Pro

[![CI](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml)
[![License: Baska-Pro Personal Use](https://img.shields.io/badge/License-Baska--Pro%20Personal%20Use%201.0-blue.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4?style=flat-square)](#requirements)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square)](#requirements)

**RemotePC Pro v2.0.0** is an administration utility for Windows PCs you own or are explicitly authorized to manage. It combines an allowlisted Telegram bot with a web dashboard authenticated by Telegram-delivered OTP.

> Use only on systems you own or administer with explicit authorization. This project is not a Windows security boundary and does not replace RDP, WDAC, Group Policy, VPNs, or enterprise endpoint management.

## Highlights

- Telegram Chat ID allowlist.
- Web dashboard with Chat ID + Telegram OTP authentication.
- CSRF protection, rate limiting, hardened response headers, and session controls.
- CPU, memory, disk, battery, network, uptime, and process status.
- Windows power/audio/local utility controls.
- Optional elevated administration functions for installations that explicitly enable them.
- Rotating logs and single-instance protection.
- Optional FFmpeg/NirCmd integration.
- Task Scheduler support is explicit/manual; the repository installer does not silently enable startup.
- Runtime configuration is stored under `%LOCALAPPDATA%\RemotePCPro`.

## Safer public defaults

The repository package uses conservative defaults:

```json
{
  "dashboard": {"host": "127.0.0.1"},
  "features": {
    "advanced_commands": false,
    "web_file_manager": false
  }
}
```

Do not expose the dashboard directly to the public internet. Prefer a private network/VPN, or a properly secured TLS reverse proxy.

## Requirements

- Windows 10/11
- Python 3.11+
- Telegram bot when Telegram control is enabled
- FFmpeg only for media features that require it
- NirCmd optional

## Install

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

See [docs/INSTALLATION.md](docs/INSTALLATION.md) and [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Security

No Telegram token, personal Chat ID, secret key, runtime configuration, log, recording, screenshot, or third-party binary belongs in Git.

See [SECURITY.md](SECURITY.md) and [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md).

## License

BASKA-PRO PERSONAL USE LICENSE Version 1.0.
