from flask import *
from auth import login_user, send_otp, reset_password, create_admin
from state import ADMINS,is_super,is_readonly,set_alert,get_alert
from railway import *
from audit import ACTIVITY, log_action
import os

app=Flask(__name__)
app.secret_key="railway-ui"

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if login_user(request.form["user"],request.form["pass"]):
            session["u"]=request.form["user"]
            return redirect("/dashboard")
    return render_template("login.html",alert=get_alert())

@app.route("/dashboard")
def dashboard():
    if "u" not in session: return redirect("/")
    return render_template("dashboard.html",projects=projects(),user=session["u"],alert=get_alert())

@app.route("/project/<pid>")
def project(pid):
    return render_template("services.html",services=services(pid),user=session["u"],readonly=is_readonly(session["u"]))

@app.route("/service/<sid>")
def service(sid):
    return render_template("service.html",sid=sid,user=session["u"])

@app.route("/api/logs/<sid>")
def api_logs(sid): return jsonify(logs(sid))

@app.route("/api/metrics/<sid>")
def api_metrics(sid): return jsonify(metrics(sid))

@app.route("/action",methods=["POST"])
def act():
    if is_readonly(session["u"]):
        set_alert("⛔ Read only admin")
        return redirect(request.referrer)
    action(request.form["sid"],request.form["a"])
    log_action(session["u"],request.form["a"])
    return redirect(request.referrer)

@app.route("/admins",methods=["GET","POST"])
def admins():
    if not is_super(session["u"]): return redirect("/dashboard")
    if request.method=="POST":
        send_otp("Create Admin")
        set_alert(create_admin(request.form["user"],request.form["pass"],request.form["role"],request.form["otp"]))
    return render_template("admins.html",admins=ADMINS,user=session["u"],alert=get_alert())

@app.route("/activity")
def activity():
    if not is_super(session["u"]): return redirect("/dashboard")
    return render_template("activity.html",logs=ACTIVITY,user=session["u"])

@app.route("/forgot",methods=["GET","POST"])
def forgot():
    if request.method=="POST":
        send_otp("Password Reset")
        set_alert("📩 OTP Telegram par bhej diya (10 min valid)")
        return redirect("/reset")
    return render_template("forgot.html",alert=get_alert())

@app.route("/reset",methods=["GET","POST"])
def reset():
    if request.method=="POST":
        set_alert(reset_password(request.form["user"],request.form["otp"],request.form["pass"]))
        return redirect("/")
    return render_template("reset.html",alert=get_alert())

@app.route("/logout")
def logout():
    session.clear()
    set_alert("👋 Logged out")
    return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",8080)))
