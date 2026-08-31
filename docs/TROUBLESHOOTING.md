# Troubleshooting

## Bot does not start

Confirm `%LOCALAPPDATA%\RemotePCPro\RemotePC.config.json` contains a valid `bot_token` and at least one `allowed_chat_ids` entry. Also verify internet access to Telegram.

## Dashboard is not reachable from another device

This is expected with the default `127.0.0.1` bind address. The public edition is localhost-only by default. Do not change this merely to expose the service directly to the internet; use a secured private network/VPN or TLS reverse proxy.

## OTP is not received

Check the bot token, allowed Chat ID, Telegram connectivity, and rate limits. Wait several minutes after repeated OTP requests.

## Lock/restart/shutdown fails

RemotePC Pro uses the permissions of the Windows account running it. Confirm the account may perform the requested action. Telegram restart/shutdown also require the literal `confirm` argument.

## CI fails

Run locally:

```powershell
python -m py_compile remotepc_pro.py scripts\check_release.py
python scripts\check_release.py
python remotepc_pro.py --version
```
