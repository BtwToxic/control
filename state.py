import time, random

ADMINS = {
    "dev": {"password": "dev123", "role": "super"}
}

ALERT = None
OTP = None
OTP_TIME = None
OTP_VALID = 600

def set_alert(msg):
    global ALERT
    ALERT = msg

def get_alert():
    global ALERT
    a = ALERT
    ALERT = None
    return a

def is_super(u):
    return ADMINS.get(u, {}).get("role") == "super"

def is_readonly(u):
    return ADMINS.get(u, {}).get("role") == "readonly"

def gen_otp():
    global OTP, OTP_TIME
    OTP = str(random.randint(100000,999999))
    OTP_TIME = time.time()
    return OTP

def verify_otp(code):
    if not OTP:
        return False, "No OTP requested"
    if time.time() - OTP_TIME > OTP_VALID:
        return False, "OTP expired"
    if code != OTP:
        return False, "Wrong OTP"
    return True, "OTP OK"
