# RemotePC Pro v2.0.0

Initial public release of RemotePC Pro.

## Highlights

- Owner-only Telegram access using an allowlist of trusted Chat IDs.
- Local web dashboard authenticated with Telegram-delivered OTP.
- Windows system status: CPU, RAM, disk, hostname, and uptime.
- Limited power controls: lock, restart, and shutdown.
- Restart/shutdown require explicit confirmation.
- Dashboard binds to `127.0.0.1` by default.
- Runtime configuration is stored outside the repository under `%LOCALAPPDATA%\RemotePCPro`.
- Installer does not silently create Scheduled Tasks or hidden startup entries.
- GitHub Actions checks syntax, version consistency, credential leaks, repository hygiene, and capability surface.

## Public-edition security boundary

The public edition intentionally does not include arbitrary shell or command execution, file browsing/transfer, screenshot/webcam/audio capture, keyboard/mouse injection, credential collection, or hidden persistence.

## Requirements

- Windows 10 or Windows 11
- Python 3.11+
- Telegram bot for Telegram control and dashboard OTP

## Installation

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

See `README.md`, `docs/INSTALLATION.md`, and `docs/CONFIGURATION.md` for setup details.

## License

BASKA-PRO PERSONAL USE LICENSE Version 1.0.
