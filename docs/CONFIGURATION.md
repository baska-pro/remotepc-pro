# Configuration

Runtime configuration:

```text
%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json
```

Start from `RemotePC.config.example.json`.

## Required values

- `bot_token`: Telegram bot token.
- `allowed_chat_ids`: Telegram numeric account IDs allowed to control the application.

## Recommended public-package defaults

```json
{
  "dashboard": {
    "host": "127.0.0.1",
    "secure_cookie": false,
    "trust_proxy_headers": false
  },
  "features": {
    "advanced_commands": false,
    "web_file_manager": false
  }
}
```

If a reverse proxy is used, configure TLS, authentication, trusted proxy handling, and network ACLs correctly before changing bind/cookie settings.

Never commit the runtime config.
