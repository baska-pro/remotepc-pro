# RemotePC Pro

[![CI](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml)
[![License: Baska-Pro Personal Use](https://img.shields.io/badge/License-Baska--Pro%20Personal%20Use%201.0-blue.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4?style=flat-square)](#persyaratan)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square)](#persyaratan)

> [English documentation](README.en.md)

**RemotePC Pro v2.0.0** adalah utilitas owner-only untuk memantau PC Windows melalui Telegram dan dashboard web, dengan kontrol power terbatas serta autentikasi Chat ID + OTP Telegram.

> Gunakan hanya pada PC yang Anda miliki atau kelola dengan izin eksplisit. RemotePC Pro bukan pengganti RDP, VPN, WDAC, Group Policy, atau endpoint-management enterprise.

## Fitur

- Telegram bot dengan allowlist Chat ID.
- Dashboard web dengan Chat ID + OTP Telegram.
- CSRF protection, session security, rate limiting, dan security headers.
- Status CPU, RAM, disk, hostname, dan uptime.
- Kontrol terbatas: lock Windows, restart, dan shutdown.
- Restart/shutdown dari Telegram memerlukan kata `confirm`; dashboard meminta konfirmasi browser.
- Dashboard bind ke `127.0.0.1` secara default.
- Config runtime disimpan di `%LOCALAPPDATA%\RemotePCPro`.
- Tidak membuat Scheduled Task atau hidden startup entry saat instalasi.
- CI memeriksa syntax, versi, credential leak, repository hygiene, dan capability surface.

## Yang sengaja tidak disertakan

Public edition **tidak menyediakan** arbitrary shell/command execution, file manager atau transfer file, screenshot/webcam/audio capture, keyboard/mouse injection, credential collection, maupun hidden persistence.

## Persyaratan

- Windows 10/11.
- Python 3.11+.
- Telegram bot untuk kontrol Telegram dan OTP dashboard.

## Instalasi

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Installer membuat virtual environment, memasang dependency, menyalin aplikasi ke `%LOCALAPPDATA%\Programs\RemotePCPro`, dan membuat config awal tanpa credential.

## Konfigurasi

Edit:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Isi minimal:

```json
{
  "bot_token": "TOKEN_BOT_ANDA",
  "allowed_chat_ids": ["CHAT_ID_ANDA"]
}
```

Jangan commit config runtime. Contoh lengkap ada di [`RemotePC.config.example.json`](RemotePC.config.example.json).

## Menjalankan

```powershell
%LOCALAPPDATA%\Programs\RemotePCPro\.venv\Scripts\python.exe `
  %LOCALAPPDATA%\Programs\RemotePCPro\remotepc_pro.py
```

Perintah Telegram:

```text
/start
/help
/status
/dashboard
/lock
/restart confirm
/shutdown confirm
```

CLI:

```powershell
python remotepc_pro.py --version
python remotepc_pro.py --diagnostics
python remotepc_pro.py --no-dashboard
```

## Dokumentasi

- [Installation](docs/INSTALLATION.md)
- [Configuration](docs/CONFIGURATION.md)
- [Security Model](docs/SECURITY_MODEL.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Security Policy](SECURITY.md)

## License

BASKA-PRO PERSONAL USE LICENSE Version 1.0. Penggunaan personal/private/non-commercial diperbolehkan sesuai `LICENSE`; redistribusi, rebranding, SaaS, dan penggunaan komersial memerlukan izin tertulis.
