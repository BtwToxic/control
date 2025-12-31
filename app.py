from flask import (
    Flask, render_template, request,
    redirect, session, jsonify
)
import os

from auth import login_user, send_otp, create_admin
from state import (
    ADMINS, is_super, is_readonly,
    get_alert, set_alert
)
from railway import (
    list_projects, list_services,
    service_logs, service_metrics,
    start_service, stop_service, restart_service
)
from audit import log_action

app = Flask(__name__)
app.secret_key = "railway-panel-final"

# ================= AUTH =================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if login_user(
            request.form.get("user"),
            request.form.get("pass")
        ):
            session["user"] = request.form["user"]
            return redirect("/dashboard")

    return render_template(
        "login.html",
        alert=get_alert()
    )

@app.route("/logout")
def logout():
    user = session.get("user")
    if user:
        log_action(user, "logout")
    session.clear()
    set_alert("👋 Logged out successfully")
    return redirect("/")

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        projects=list_projects(),
        user=session["user"],
        alert=get_alert()
    )

# ================= PROJECT → SERVICES =================

@app.route("/project/<project_id>")
def project_services(project_id):
    if "user" not in session:
        return redirect("/")

    return render_template(
        "services.html",
        services=list_services(project_id),
        pid=project_id,
        user=session["user"],
        readonly=is_readonly(session["user"])
    )

# ================= SERVICE PAGE =================

@app.route("/service/<service_id>")
def service_page(service_id):
    if "user" not in session:
        return redirect("/")

    return render_template(
        "service.html",
        sid=service_id,
        user=session["user"]
    )

# ================= API (AJAX) =================

@app.route("/api/logs/<service_id>")
def api_logs(service_id):
    return jsonify(service_logs(service_id))

@app.route("/api/metrics/<service_id>")
def api_metrics(service_id):
    return jsonify(service_metrics(service_id))

# ================= SERVICE ACTIONS =================

@app.route("/action", methods=["POST"])
def service_action():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    if is_readonly(user):
        set_alert("⛔ Read-only admin cannot perform actions")
        return redirect(request.referrer)

    service_id = request.form["sid"]
    action = request.form["a"]

    if action == "start":
        start_service(service_id)
    elif action == "stop":
        stop_service(service_id)
    elif action == "restart":
        restart_service(service_id)

    log_action(user, f"{action} service {service_id}")
    set_alert("⚙️ Action executed")
    return redirect(request.referrer)

# ================= ADMINS (SUPER ONLY) =================

@app.route("/admins", methods=["GET", "POST"])
def admins():
    if not is_super(session.get("user")):
        return redirect("/dashboard")

    if request.method == "POST":
        send_otp("Create Admin")
        create_admin(
            request.form["user"],
            request.form["pass"],
            request.form["role"],
            request.form["otp"]
        )

    return render_template(
        "admins.html",
        admins=ADMINS,
        alert=get_alert(),
        user=session["user"]
    )

# ================= USER PAGE =================

@app.route("/coming")
def coming():
    if "user" not in session:
        return redirect("/")
    return render_template(
        "coming.html",
        user=session["user"]
    )

# ================= START =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
