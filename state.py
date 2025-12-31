import time, random

ADMINS = {
    "dev": {"password":"dev123","role":"super"}
}

ALERT=None

RESET_OTP=None
RESET_TIME=None
RESET_VALID=600

def set_alert(m):
    global ALERT
    ALERT=m

def get_alert():
    global ALERT
    a=ALERT
    ALERT=None
    return a

def is_super(u):
    return ADMINS.get(u,{}).get("role")=="super"

def is_readonly(u):
    return ADMINS.get(u,{}).get("role")=="readonly"

def gen_otp():
    global RESET_OTP, RESET_TIME
    RESET_OTP=str(random.randint(100000,999999))
    RESET_TIME=time.time()
    return RESET_OTP

def verify_otp(code):
    if not RESET_OTP:
        return False,"No OTP"
    if time.time()-RESET_TIME>RESET_VALID:
        return False,"OTP expired"
    if code!=RESET_OTP:
        return False,"Wrong OTP"
    return True,"OK"
