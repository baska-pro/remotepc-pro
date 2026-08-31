# Changelog

## 2.0.0 - 2026-08-31

### Added
- Telegram allowlist and secure web dashboard with Telegram OTP.
- Windows telemetry, local control utilities, process information, and logging.
- GitHub-ready packaging, documentation, installer/uninstaller, and CI.

### Security / packaging
- Public package stores runtime configuration under `%LOCALAPPDATA%\RemotePCPro`.
- Public default dashboard bind address changed to `127.0.0.1`.
- `advanced_commands` defaults to disabled.
- `web_file_manager` defaults to disabled.
- Runtime credentials and generated files are excluded from Git.
- Installer does not create automatic startup persistence.
