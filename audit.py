import time, requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

ACTIVITY=[]

def log_action(user, action):
    ACTIVITY.append({
        "user":user,
        "action":action,
        "time":time.ctime()
    })
    if TELEGRAM_BOT_TOKEN:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id":TELEGRAM_CHAT_ID,"text":f"🧾 {user} → {action}"},
                timeout=5
            )
        except: pass
