import requests
from flask import request
from state import ADMINS, set_alert, gen_otp, verify_otp
from audit import log_action
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def login_user(u,p):
    if u not in ADMINS or ADMINS[u]["password"]!=p:
        set_alert("❌ Invalid credentials")
        return False
    set_alert("✅ Login successful")
    log_action(u,"login")
    return True

def send_otp(reason):
    code=gen_otp()
    if TELEGRAM_BOT_TOKEN:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={
                "chat_id":TELEGRAM_CHAT_ID,
                "text":f"🔐 {reason}\nOTP: {code}\nIP: {request.remote_addr}"
            },
            timeout=5
        )

def reset_password(user,otp,newp):
    if user not in ADMINS:
        return "❌ User nahi mila"
    ok,msg=verify_otp(otp)
    if not ok: return msg
    ADMINS[user]["password"]=newp
    log_action(user,"password reset")
    return "✅ Password reset successful"

def create_admin(u,p,role,otp):
    ok,msg=verify_otp(otp)
    if not ok: return msg
    ADMINS[u]={"password":p,"role":role}
    log_action("dev",f"created admin {u}")
    return "✅ Admin created"
