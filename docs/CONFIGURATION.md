# Configuration

Runtime configuration is stored at:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Start from `RemotePC.config.example.json`.

## Required values

- `bot_token`: Telegram bot token.
- `allowed_chat_ids`: Telegram account IDs allowed to use the bot and request dashboard OTPs.

Example:

```json
{
  "bot_token": "TOKEN_BOT_ANDA",
  "allowed_chat_ids": ["123456789"],
  "dashboard": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8765,
    "session_hours": 8,
    "otp_expire_seconds": 300,
    "secure_cookie": false,
    "trust_proxy_headers": false
  },
  "features": {
    "power_controls": true,
    "startup_message": true
  },
  "secret_key": ""
}
```

`secret_key` may remain empty on first run; RemotePC Pro generates one automatically. Keep the dashboard bound to localhost unless you intentionally place it behind a secured private network/VPN or correctly configured TLS reverse proxy.

Never commit the runtime configuration.
