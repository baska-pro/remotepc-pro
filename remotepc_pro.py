#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RemotePC Pro: owner-only Windows status dashboard and safe power control.

Public edition intentionally excludes arbitrary shell, file browsing/transfer,
screenshot/webcam/audio capture, input injection, credential collection, and
hidden persistence.
"""
from __future__ import annotations
import argparse, hashlib, hmac, json, os, secrets, socket, subprocess, sys, threading, time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

VERSION = "2.0.0"
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
STATE_DIR = Path(os.getenv("LOCALAPPDATA", str(Path.home()))) / "RemotePCPro"
CONFIG_PATH = Path(os.getenv("REMOTEPC_CONFIG", str(STATE_DIR / "RemotePC.config.json")))
STATE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "bot_token": "", "allowed_chat_ids": [],
    "dashboard": {"enabled": True, "host": "127.0.0.1", "port": 8765,
                  "session_hours": 8, "otp_expire_seconds": 300,
                  "secure_cookie": False, "trust_proxy_headers": False},
    "features": {"power_controls": True, "startup_message": True},
    "secret_key": ""
}

def merge(a, b):
    out = json.loads(json.dumps(a))
    for k, v in (b or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

def save_config(c):
    p = CONFIG_PATH.with_suffix(".tmp"); p.write_text(json.dumps(c, indent=2)+"\n", encoding="utf-8"); os.replace(p, CONFIG_PATH)

def load_config():
    c = merge(DEFAULT_CONFIG, json.loads(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {})
    if not c["secret_key"]: c["secret_key"] = secrets.token_urlsafe(48); save_config(c)
    return c

CONFIG = load_config()
BOT_TOKEN = os.getenv("REMOTEPC_BOT_TOKEN", "").strip() or str(CONFIG.get("bot_token", "")).strip()
ALLOWED = {str(x).strip() for x in CONFIG.get("allowed_chat_ids", []) if str(x).strip()}

def deps():
    import importlib.util
    req = {"psutil":"psutil>=5.9,<8","flask":"Flask>=3.1,<4","waitress":"waitress>=3,<4","telegram":"python-telegram-bot>=22.6,<23","requests":"requests>=2.31,<3"}
    missing=[p for m,p in req.items() if importlib.util.find_spec(m) is None]
    if missing: subprocess.check_call([sys.executable,"-m","pip","install","--disable-pip-version-check",*missing])

def snapshot():
    import psutil
    vm=psutil.virtual_memory(); boot=datetime.fromtimestamp(psutil.boot_time()); root=os.environ.get("SystemDrive","C:")+"\\"
    try: d=psutil.disk_usage(root); disk={"percent":d.percent,"total":d.total,"used":d.used}
    except Exception: disk={"percent":0,"total":0,"used":0}
    return {"hostname":socket.gethostname(),"cpu":psutil.cpu_percent(.12),"ram":vm.percent,"disk":disk,"uptime":int((datetime.now()-boot).total_seconds())}

def power(action):
    if not CONFIG["features"].get("power_controls", True): raise PermissionError("Power control disabled")
    cmds={"lock":["rundll32.exe","user32.dll,LockWorkStation"],"shutdown":["shutdown","/s","/t","0"],"restart":["shutdown","/r","/t","0"]}
    if action not in cmds: raise ValueError("Action not allowed")
    subprocess.Popen(cmds[action], creationflags=CREATE_NO_WINDOW)

def allowed(update):
    try: return str(update.effective_user.id) in ALLOWED
    except Exception: return False

async def start(update, context):
    if not allowed(update): return await update.message.reply_text("Akses ditolak.")
    await update.message.reply_text("RemotePC Pro\n/status\n/dashboard\n/lock\n/shutdown confirm\n/restart confirm")

async def status(update, context):
    if not allowed(update): return await update.message.reply_text("Akses ditolak.")
    s=snapshot(); await update.message.reply_text(f"Host: {s['hostname']}\nCPU: {s['cpu']:.1f}%\nRAM: {s['ram']:.1f}%\nDisk: {s['disk']['percent']:.1f}%\nUptime: {timedelta(seconds=s['uptime'])}")

async def dashboard_cmd(update, context):
    if not allowed(update): return await update.message.reply_text("Akses ditolak.")
    d=CONFIG["dashboard"]; await update.message.reply_text(f"Dashboard: http://{d['host']}:{d['port']}\nLogin: Chat ID + OTP Telegram")

async def lock_cmd(update, context):
    if not allowed(update): return await update.message.reply_text("Akses ditolak.")
    power("lock"); await update.message.reply_text("Layar dikunci.")

async def destructive(update, context, action):
    if not allowed(update): return await update.message.reply_text("Akses ditolak.")
    if not context.args or context.args[0].lower()!="confirm": return await update.message.reply_text(f"Gunakan /{action} confirm")
    await update.message.reply_text(f"Perintah {action} dikirim."); power(action)

async def shutdown_cmd(u,c): await destructive(u,c,"shutdown")
async def restart_cmd(u,c): await destructive(u,c,"restart")

def bot_app():
    from telegram.ext import Application, CommandHandler
    a=Application.builder().token(BOT_TOKEN).build()
    for n,f in [("start",start),("help",start),("status",status),("dashboard",dashboard_cmd),("lock",lock_cmd),("shutdown",shutdown_cmd),("restart",restart_cmd)]: a.add_handler(CommandHandler(n,f))
    return a

OTP={}; OTP_LOCK=threading.RLock(); RATE=defaultdict(deque); RATE_LOCK=threading.RLock()
def rate(key,limit,window):
    now=time.time()
    with RATE_LOCK:
        q=RATE[key]
        while q and q[0]<now-window:q.popleft()
        if len(q)>=limit:return False
        q.append(now);return True

def ohash(code): return hmac.new(CONFIG["secret_key"].encode(),code.encode(),hashlib.sha256).hexdigest()
def send(chat,text):
    import requests
    try:return requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data={"chat_id":chat,"text":text},timeout=15).ok
    except Exception:return False

def issue_otp(chat,ip):
    if chat not in ALLOWED:return "Jika Chat ID terdaftar, OTP telah dikirim."
    if not rate("otp:"+chat,4,600):return "Terlalu banyak permintaan OTP."
    code=f"{secrets.randbelow(1000000):06d}"; ttl=max(60,int(CONFIG["dashboard"]["otp_expire_seconds"]))
    with OTP_LOCK:OTP[chat]={"h":ohash(code),"exp":time.time()+ttl,"tries":0}
    return "OTP dikirim." if send(chat,f"RemotePC Pro OTP: {code}\nIP: {ip}\nBerlaku {ttl//60} menit") else "Gagal mengirim OTP."

def verify(chat,code):
    with OTP_LOCK:
        x=OTP.get(chat)
        if not x or time.time()>x["exp"]:OTP.pop(chat,None);return False
        x["tries"]+=1
        if x["tries"]>5:OTP.pop(chat,None);return False
        ok=hmac.compare_digest(x["h"],ohash(code))
        if ok:OTP.pop(chat,None)
        return ok

LOGIN="""<!doctype html><meta name=viewport content='width=device-width'><style>body{font-family:Segoe UI;background:#09111a;color:#eee;display:grid;place-items:center;min-height:100vh}.c{background:#111d29;padding:24px;border-radius:18px;width:min(400px,86vw)}input,button{width:100%;box-sizing:border-box;padding:12px;margin:6px 0;border-radius:9px;border:1px solid #345;background:#08131d;color:white}button{background:#1769aa}</style><div class=c><h2>RemotePC Pro</h2><p>{msg}</p><form method=post><input type=hidden name=csrf_token value='{csrf}'><input name=chat placeholder='Chat ID'><input name=otp placeholder='OTP'><button name=step value=request>Kirim OTP</button><button name=step value=verify>Masuk</button></form></div>"""
DASH="""<!doctype html><meta name=viewport content='width=device-width'><meta name=csrf content='{csrf}'><style>body{font-family:Segoe UI;background:#09111a;color:#eee;max-width:900px;margin:auto;padding:24px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.c{background:#111d29;padding:18px;border-radius:14px}button{padding:10px;border:0;border-radius:8px;background:#1769aa;color:white;margin:4px}.d{background:#a32d36}</style><h1>RemotePC Pro</h1><div class=g><div class=c>CPU <b id=cpu>-</b></div><div class=c>RAM <b id=ram>-</b></div><div class=c>Disk <b id=disk>-</b></div><div class=c>Host <b id=host>-</b></div></div><div class=c style='margin-top:10px'><button onclick="act('lock')">Lock</button><button class=d onclick="ask('restart')">Restart</button><button class=d onclick="ask('shutdown')">Shutdown</button> <a href=/logout>Logout</a></div><script>let csrf=document.querySelector('meta[name=csrf]').content;async function st(){let r=await fetch('/api/status'),j=await r.json();if(!r.ok){location='/login';return}cpu.textContent=j.data.cpu.toFixed(1)+'%';ram.textContent=j.data.ram.toFixed(1)+'%';disk.textContent=j.data.disk.percent.toFixed(1)+'%';host.textContent=j.data.hostname}async function act(a){let r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:a})}),j=await r.json();alert(j.message||j.error)}function ask(a){if(confirm('Konfirmasi '+a+'?'))act(a)}st();setInterval(st,5000)</script>"""

def dashboard_app():
    from flask import Flask,request,session,redirect,url_for,jsonify,render_template_string
    app=Flask("RemotePCPro");app.secret_key=CONFIG["secret_key"];app.config.update(SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE="Strict",SESSION_COOKIE_SECURE=bool(CONFIG["dashboard"].get("secure_cookie")),PERMANENT_SESSION_LIFETIME=timedelta(hours=int(CONFIG["dashboard"].get("session_hours",8))))
    def ip():
        if CONFIG["dashboard"].get("trust_proxy_headers") and request.headers.get("X-Forwarded-For"):return request.headers["X-Forwarded-For"].split(",")[0].strip()[:64]
        return (request.remote_addr or "unknown")[:64]
    def csrf():
        if not session.get("csrf"):session["csrf"]=secrets.token_urlsafe(24)
        return session["csrf"]
    def cv():
        a=request.headers.get("X-CSRF-Token") or request.form.get("csrf_token") or "";b=session.get("csrf","");return bool(a and b and hmac.compare_digest(a,b))
    def auth(fn):
        @wraps(fn)
        def w(*a,**k):
            if not session.get("ok") or str(session.get("chat")) not in ALLOWED:return (jsonify({"error":"AUTH_REQUIRED"}),401) if request.path.startswith('/api/') else redirect(url_for('login'))
            return fn(*a,**k)
        return w
    @app.after_request
    def hdr(r):r.headers.update({"X-Frame-Options":"DENY","X-Content-Type-Options":"nosniff","Referrer-Policy":"no-referrer","Cache-Control":"no-store"});return r
    @app.route('/login',methods=['GET','POST'])
    def login():
        msg=""
        if request.method=='POST':
            if not cv():msg="Form kedaluwarsa."
            elif not rate('login:'+ip(),10,600):msg="Terlalu banyak percobaan."
            else:
                chat=request.form.get('chat','').strip();step=request.form.get('step','')
                if step=='request':msg=issue_otp(chat,ip())
                elif step=='verify' and verify(chat,request.form.get('otp','')):session.clear();session['ok']=True;session['chat']=chat;session.permanent=True;csrf();return redirect('/')
                elif step=='verify':msg="OTP tidak valid."
        return render_template_string(LOGIN,msg=msg,csrf=csrf())
    @app.route('/')
    @auth
    def home():return render_template_string(DASH,csrf=csrf())
    @app.route('/logout')
    def logout():session.clear();return redirect('/login')
    @app.route('/healthz')
    def health():return jsonify({"ok":True,"version":VERSION})
    @app.route('/api/status')
    @auth
    def api_status():return jsonify({"ok":True,"data":snapshot()})
    @app.route('/api/action',methods=['POST'])
    @auth
    def action():
        if not cv():return jsonify({"error":"CSRF_INVALID"}),403
        a=str((request.get_json(silent=True) or {}).get('action',''))
        try:power(a);return jsonify({"ok":True,"message":f"Perintah {a} dikirim."})
        except Exception as e:return jsonify({"error":str(e)}),400
    return app

def start_dashboard():
    if not CONFIG["dashboard"].get("enabled",True):return
    from waitress import serve
    d=CONFIG["dashboard"]
    threading.Thread(target=lambda:serve(dashboard_app(),host=str(d["host"]),port=int(d["port"]),threads=6),daemon=True,name='dashboard').start()

def diagnostics():print(json.dumps({"version":VERSION,"config":str(CONFIG_PATH),"allowed_chat_ids_count":len(ALLOWED),"dashboard":CONFIG["dashboard"]},indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument('--version',action='store_true');p.add_argument('--diagnostics',action='store_true');p.add_argument('--no-dashboard',action='store_true');a=p.parse_args()
    if a.version:return print(VERSION)
    if a.diagnostics:return diagnostics()
    if os.name!='nt':raise RuntimeError("RemotePC Pro ditujukan untuk Windows 10/11.")
    deps()
    if not BOT_TOKEN or not ALLOWED:raise RuntimeError(f"Atur bot_token dan allowed_chat_ids di {CONFIG_PATH}")
    if not a.no_dashboard:start_dashboard()
    if CONFIG["features"].get("startup_message",True):send(sorted(ALLOWED)[0],f"RemotePC Pro v{VERSION} aktif.")
    bot_app().run_polling(drop_pending_updates=False)

if __name__=='__main__':main()
