# RemotePC Pro

[![CI](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml)
[![License: Baska-Pro Personal Use](https://img.shields.io/badge/License-Baska--Pro%20Personal%20Use%201.0-blue.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4?style=flat-square)](#requirements)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square)](#requirements)

**RemotePC Pro v2.0.0** is an owner-only Windows monitoring utility with Telegram control and a web dashboard authenticated by an allowlisted Chat ID and Telegram OTP.

> Use only on systems you own or explicitly administer. RemotePC Pro is not a replacement for RDP, VPNs, WDAC, Group Policy, or enterprise endpoint management.

## Highlights

- Telegram Chat ID allowlist.
- Web dashboard with Telegram-delivered OTP.
- CSRF protection, rate limiting, secure session controls, and response security headers.
- CPU, memory, disk, hostname, and uptime monitoring.
- Limited Windows controls: lock, restart, and shutdown.
- Telegram restart/shutdown require `confirm`; the dashboard requires browser confirmation.
- Dashboard binds to `127.0.0.1` by default.
- Runtime configuration is stored under `%LOCALAPPDATA%\RemotePCPro`.
- The installer creates no Scheduled Task or hidden startup entry.
- CI validates syntax, versions, credential hygiene, repository hygiene, and the public capability surface.

## Intentionally excluded

The public edition does **not** include arbitrary shell/command execution, file browsing/transfer, screenshot/webcam/audio capture, keyboard/mouse injection, credential collection, or hidden persistence.

## Requirements

- Windows 10/11
- Python 3.11+
- A Telegram bot for Telegram control and dashboard OTP

## Install

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Edit `%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json`, then start the installed application. See [docs/INSTALLATION.md](docs/INSTALLATION.md) and [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Telegram commands

```text
/start
/help
/status
/dashboard
/lock
/restart confirm
/shutdown confirm
```

## Security

Never commit Telegram tokens, Chat IDs, runtime configuration, logs, or other private data. See [SECURITY.md](SECURITY.md) and [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md).

## License

BASKA-PRO PERSONAL USE LICENSE Version 1.0.
