# Contributing

Contributions should improve reliability, documentation, compatibility, testing, accessibility, or defensive security.

Do not submit changes that add or strengthen:
- credential theft;
- stealth or hidden persistence;
- unauthorized surveillance;
- arbitrary remote shell capability;
- evasion of Windows security controls;
- secret collection or exfiltration.

Before submitting changes:

```powershell
python -m py_compile remotepc_pro.py
python scripts\check_release.py
```

Never include real Telegram tokens, Chat IDs, private hostnames, screenshots with personal data, or runtime config files.
