#!/usr/bin/env python3
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise SystemExit(f"Invalid VERSION: {version!r}")

source = (ROOT / "remotepc_pro.py").read_text(encoding="utf-8")
ast.parse(source, filename="remotepc_pro.py")
if f'VERSION = "{version}"' not in source:
    raise SystemExit("VERSION constant mismatch")

cfg = json.loads((ROOT / "RemotePC.config.example.json").read_text(encoding="utf-8"))
if cfg.get("bot_token"):
    raise SystemExit("Example config must not contain a Telegram token")
if cfg.get("allowed_chat_ids"):
    raise SystemExit("Example config must not contain personal Chat IDs")
if cfg.get("dashboard", {}).get("host") != "127.0.0.1":
    raise SystemExit("Public dashboard must bind to localhost by default")
if not isinstance(cfg.get("features", {}).get("power_controls"), bool):
    raise SystemExit("power_controls must be a boolean")

forbidden = {
    'subprocess.Popen(["cmd.exe"': "arbitrary command execution",
    'subprocess.run(["cmd.exe"': "arbitrary command execution",
    "ImageGrab": "screen capture",
    "sendDocument": "arbitrary file transfer",
    "send2trash": "remote file deletion",
    "MOUSEEVENTF_": "mouse injection",
    ".SendKeys(": "keyboard injection",
    '"schtasks"': "startup persistence",
}
for marker, capability in forbidden.items():
    if marker in source:
        raise SystemExit(f"Forbidden public-edition capability detected: {capability}")

print(f"RemotePC Pro release validation passed: {version}")
