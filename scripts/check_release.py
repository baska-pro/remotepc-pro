#!/usr/bin/env python3
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise SystemExit(f"Invalid VERSION: {version!r}")

loader = (ROOT / "remotepc_pro.py").read_text(encoding="utf-8")
ast.parse(loader, filename="remotepc_pro.py")
if f'VERSION = "{version}"' not in loader:
    raise SystemExit("VERSION constant mismatch in loader")

parts = sorted((ROOT / "src" / "remotepc_pro").glob("part*.pyfrag"))
if not parts:
    raise SystemExit("Implementation source fragments are missing")
implementation = "".join(p.read_text(encoding="utf-8") for p in parts)
ast.parse(implementation, filename="remotepc_pro_implementation.py")
if f'VERSION = "{version}"' not in implementation:
    raise SystemExit("VERSION constant mismatch in implementation")

cfg = json.loads((ROOT / "RemotePC.config.example.json").read_text(encoding="utf-8"))
if cfg.get("bot_token"):
    raise SystemExit("Example config must not contain a Telegram token")
if cfg.get("allowed_chat_ids"):
    raise SystemExit("Example config must not contain personal Chat IDs")
features = cfg.get("features", {})
if features.get("advanced_commands") is not False:
    raise SystemExit("advanced_commands must default to false in public example")
if features.get("web_file_manager") is not False:
    raise SystemExit("web_file_manager must default to false in public example")
if cfg.get("dashboard", {}).get("host") != "127.0.0.1":
    raise SystemExit("Public example dashboard must bind to localhost")

print(f"RemotePC Pro release validation passed: {version}")
