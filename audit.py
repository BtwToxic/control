import time, requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def log_action(user, action):
    if not TELEGRAM_BOT_TOKEN:
        return
    text = f"""
🧾 ADMIN ACTIVITY

User: {user}
Action: {action}
Time: {time.ctime()}
"""
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=5
        )
    except:
        pass
