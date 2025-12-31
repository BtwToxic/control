from flask import *
from auth import login_user, send_otp, create_admin
from state import ADMINS, is_super, is_readonly, get_alert, set_alert
from railway import *
from audit import log_action
import os

app=Flask(__name__)
app.secret_key="railway-panel"

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
    return render_template("services.html",services=services(pid),pid=pid,user=session["u"])

@app.route("/service/<sid>")
def service_page(sid):
    return render_template("service.html",sid=sid,user=session["u"])

@app.route("/api/logs/<sid>")
def api_logs(sid): return jsonify(logs(sid))

@app.route("/api/metrics/<sid>")
def api_metrics(sid): return jsonify(metrics(sid))

@app.route("/action",methods=["POST"])
def action():
    if is_readonly(session["u"]):
        set_alert("⛔ Read only")
        return redirect(request.referrer)
    sid=request.form["sid"]
    a=request.form["a"]
    {"start":start,"stop":stop,"restart":restart}[a](sid)
    log_action(session["u"],f"{a} {sid}")
    return redirect(request.referrer)

@app.route("/admins",methods=["GET","POST"])
def admins():
    if not is_super(session["u"]): return redirect("/dashboard")
    if request.method=="POST":
        send_otp("Create Admin")
        create_admin(request.form["user"],request.form["pass"],request.form["role"],request.form["otp"])
    return render_template("admins.html",admins=ADMINS,alert=get_alert())

@app.route("/coming")
def coming(): return render_template("coming.html")

@app.route("/logout")
def logout():
    log_action(session["u"],"logout")
    session.clear()
    return redirect("/")
