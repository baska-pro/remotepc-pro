#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RemotePC Pro source loader.

The implementation is split into plain-text source fragments under
``src/remotepc_pro`` so the public repository can keep the large single-file
application reviewable while preserving the original runtime behavior.
"""
from pathlib import Path
import sys

VERSION = "2.0.0"

if "--version" in sys.argv:
    print(VERSION)
    raise SystemExit(0)

ROOT = Path(__file__).resolve().parent
PARTS_DIR = ROOT / "src" / "remotepc_pro"
PARTS = sorted(PARTS_DIR.glob("part*.pyfrag"))
if not PARTS:
    raise RuntimeError(f"RemotePC Pro source fragments are missing: {PARTS_DIR}")

source = "".join(path.read_text(encoding="utf-8") for path in PARTS)
exec(compile(source, str(ROOT / "remotepc_pro_implementation.py"), "exec"), globals(), globals())
