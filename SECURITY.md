# Security Policy

## Scope

RemotePC Pro is intended only for Windows computers the operator owns or is explicitly authorized to manage.

## Important boundaries

- Treat the Telegram bot token as a password.
- Keep the allowlist limited to trusted Telegram accounts.
- Do not expose the dashboard directly to the public internet.
- Prefer `127.0.0.1`, a private network/VPN, or a correctly configured TLS reverse proxy.
- Keep `advanced_commands` and `web_file_manager` disabled unless there is a specific, authorized need.
- Never commit `RemotePC.config.json`, `.env`, logs, screenshots, recordings, session data, or third-party binaries.

## Reporting

Do not publish exploitable security details, credentials, or private host information in a public issue. Report security concerns privately to the repository owner.
