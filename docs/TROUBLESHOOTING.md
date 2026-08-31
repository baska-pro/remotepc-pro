# Troubleshooting

## Bot does not start

Check that the runtime config contains a valid Telegram token and at least one allowed Chat ID.

## Dashboard is not reachable

The public package binds to `127.0.0.1` by default. Open it from the same PC unless you deliberately configure a private network/reverse proxy.

## FFmpeg features fail

FFmpeg is optional and not bundled. Configure `paths.ffmpeg` or add FFmpeg to PATH.

## Permission denied

RemotePC Pro uses the privileges of the Windows account that launched it. Some system actions require additional Windows permissions.

## CI fails

Run:

```powershell
python -m py_compile remotepc_pro.py
python scripts\check_release.py
```
