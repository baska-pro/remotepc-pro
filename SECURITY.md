# Security Policy

## Scope

RemotePC Pro is intended only for Windows computers the operator owns or is explicitly authorized to manage.

## Public edition boundary

The public edition intentionally excludes arbitrary shell/command execution, file browsing/transfer, screenshot/webcam/audio capture, keyboard/mouse injection, credential collection, and hidden persistence.

Available remote actions are limited to authenticated status access plus lock, restart, and shutdown. Destructive Telegram power actions require an explicit `confirm` argument.

## Important rules

- Treat the Telegram bot token as a password.
- Keep `allowed_chat_ids` limited to trusted Telegram accounts.
- Keep the dashboard on `127.0.0.1` unless you deliberately deploy it behind a properly secured private network/VPN or TLS reverse proxy.
- Never commit `RemotePC.config.json`, `.env`, logs, tokens, Chat IDs, or other private host data.
- Review configuration and dependency changes before deploying updates.

## Reporting

Do not publish credentials, private host information, or exploitable security details in a public issue. Report security concerns privately to the repository owner.
