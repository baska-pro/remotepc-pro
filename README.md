# RemotePC Pro

[![CI](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/baska-pro/remotepc-pro/actions/workflows/ci.yml)
[![License: Baska-Pro Personal Use](https://img.shields.io/badge/License-Baska--Pro%20Personal%20Use%201.0-blue.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4?style=flat-square)](#persyaratan)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square)](#persyaratan)

> [English documentation](README.en.md)

**RemotePC Pro v2.0.0** adalah aplikasi administrasi PC Windows milik sendiri melalui Telegram dan dashboard web dengan autentikasi Chat ID + OTP.

> Gunakan hanya pada PC yang Anda miliki atau kelola dengan izin eksplisit. Project ini bukan mekanisme keamanan Windows dan bukan pengganti RDP, Windows AppLocker, WDAC, Group Policy, VPN, atau endpoint-management enterprise.

## Fitur utama

- Telegram bot dengan allowlist Chat ID.
- Dashboard web dengan login Chat ID + OTP Telegram.
- CSRF protection, session cookie, rate limiting, dan security headers.
- Status CPU, RAM, disk, baterai, network, uptime, dan proses.
- Kontrol power Windows, volume, popup, TTS, keyboard, mouse, dan utilitas lokal.
- Dashboard dan bot menyediakan sejumlah fungsi administrasi tingkat lanjut pada instalasi yang mengaktifkannya.
- Rotating log dan single-instance mutex.
- Dukungan FFmpeg/NirCmd opsional.
- Task Scheduler tersedia sebagai tindakan **manual/eksplisit**, bukan diaktifkan otomatis oleh installer repository.
- Config runtime dan credential disimpan di `%LOCALAPPDATA%\RemotePCPro`, bukan di repository.

## Default keamanan repository publik

Paket GitHub ini memakai default yang lebih konservatif daripada file kerja awal:

```json
{
  "dashboard": {
    "host": "127.0.0.1"
  },
  "features": {
    "advanced_commands": false,
    "web_file_manager": false
  }
}
```

Jangan membuka dashboard langsung ke internet. Gunakan jaringan privat/VPN atau reverse proxy yang dikonfigurasi dengan TLS dan kontrol akses yang sesuai.

## Persyaratan

- Windows 10/11.
- Python 3.11+.
- Telegram bot jika kontrol Telegram digunakan.
- FFmpeg hanya jika fitur media yang memang Anda aktifkan memerlukannya.
- NirCmd bersifat opsional.

## Instalasi

```powershell
git clone https://github.com/baska-pro/remotepc-pro.git
cd remotepc-pro
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Installer:
- membuat virtual environment;
- memasang dependency;
- menyalin aplikasi ke `%LOCALAPPDATA%\Programs\RemotePCPro`;
- membuat config awal dari contoh;
- **tidak** membuat startup persistence otomatis.

Lihat [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Konfigurasi

Edit file:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Minimal isi `bot_token` dan `allowed_chat_ids`. Jangan commit file config runtime.

Contoh aman tersedia di [`RemotePC.config.example.json`](RemotePC.config.example.json).

Lihat [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Menjalankan

```powershell
%LOCALAPPDATA%\Programs\RemotePCPro\.venv\Scripts\python.exe `
  %LOCALAPPDATA%\Programs\RemotePCPro\remotepc_pro.py
```

Cek versi:

```powershell
python remotepc_pro.py --version
```

## Struktur repository

```text
remotepc-pro/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  ├─ workflows/ci.yml
│  └─ pull_request_template.md
├─ assets/screenshots/
├─ docs/
├─ scripts/
├─ remotepc_pro.py
├─ RemotePC.config.example.json
├─ install.ps1
├─ uninstall.ps1
├─ requirements.txt
├─ VERSION
├─ CHANGELOG.md
├─ SECURITY.md
├─ CONTRIBUTING.md
├─ LICENSE
└─ README.md
```

## Keamanan

Repository tidak menyertakan token Telegram, Chat ID pribadi, secret key, config runtime, log, rekaman, screenshot, maupun binary pihak ketiga.

Untuk laporan kerentanan dan model keamanan, baca:
- [SECURITY.md](SECURITY.md)
- [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md)

## Batasan

RemotePC Pro bekerja pada sesi user Windows dan hak akses proses yang menjalankannya. Administrator Windows tetap dapat menghentikan program atau mengubah konfigurasi. Beberapa tindakan sistem membutuhkan privilege yang sesuai.

## License

BASKA-PRO PERSONAL USE LICENSE Version 1.0. Penggunaan personal/private/non-commercial diperbolehkan sesuai ketentuan LICENSE; redistribusi, rebranding, SaaS, dan penggunaan komersial memerlukan izin tertulis.
