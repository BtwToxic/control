import requests, time
from flask import request
from state import ADMINS, set_alert, gen_otp, verify_otp
from audit import log_action
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def login_user(u,p):
    if u not in ADMINS or ADMINS[u]["password"] != p:
        set_alert("❌ Invalid login")
        return False
    set_alert("✅ Login successful")
    log_action(u, "login")
    return True

def send_otp(action):
    code = gen_otp()
    msg = f"""
🔐 {action}

OTP: {code}
IP: {request.remote_addr}
Device: {request.headers.get("User-Agent")}
Time: {time.ctime()}
"""
    if TELEGRAM_BOT_TOKEN:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=5
        )

def create_admin(user, pwd, role, otp):
    ok,_ = verify_otp(otp)
    if not ok:
        set_alert("❌ OTP invalid")
        return
    ADMINS[user] = {"password": pwd, "role": role}
    set_alert("✅ Admin created")
    log_action("dev", f"create admin {user} ({role})")
