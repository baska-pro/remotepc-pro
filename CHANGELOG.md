# Changelog

## 2.0.0 - 2026-08-31

### Added
- Owner-only Telegram bot with Chat ID allowlist.
- Secure dashboard login using Chat ID + short-lived Telegram OTP.
- CPU, RAM, disk, hostname, and uptime monitoring.
- Limited Windows lock, restart, and shutdown controls.
- CSRF protection, rate limiting, session protection, and security headers.
- Installer, uninstaller, documentation, release validator, and GitHub Actions CI.

### Security
- Dashboard binds to `127.0.0.1` by default.
- Restart/shutdown from Telegram require explicit confirmation.
- Runtime configuration is kept outside the repository under `%LOCALAPPDATA%\RemotePCPro`.
- Installer creates no automatic Scheduled Task or hidden startup entry.
- Public edition excludes arbitrary shell, remote file browsing/transfer, screen/camera/audio capture, input injection, credential collection, and hidden persistence.
