from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Complaint, Assignment, Notification

maintenance_bp = Blueprint("maintenance", __name__, url_prefix="/maintenance")

def staff_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "maintenance":
            flash("Maintenance staff access required.", "danger")
            return redirect(url_for("auth.home"))
        return fn(*args, **kwargs)
    return wrapper

@maintenance_bp.route("/dashboard")
@staff_required
def dashboard():
    assignments = Assignment.query.filter_by(staff_id=current_user.id).order_by(Assignment.assigned_at.desc()).all()
    return render_template("maintenance/dashboard.html", assignments=assignments)

@maintenance_bp.route("/complaints/<int:complaint_id>", methods=["GET", "POST"])
@staff_required
def complaint_detail(complaint_id):
    assignment = Assignment.query.filter_by(complaint_id=complaint_id, staff_id=current_user.id).first_or_404()
    complaint = assignment.complaint

    if request.method == "POST":
        status = request.form["status"]
        allowed = {"Assigned", "In Progress", "Resolved"}
        if status not in allowed:
            flash("Invalid status.", "danger")
            return redirect(url_for("maintenance.complaint_detail", complaint_id=complaint.id))

        complaint.status = status
        complaint.resolution_notes = request.form.get("resolution_notes")

        db.session.add(Notification(
            user_id=complaint.student_id,
            message=f"Complaint #{complaint.id} status changed to {status}."
        ))
        db.session.commit()

        flash("Complaint updated.", "success")
        return redirect(url_for("maintenance.dashboard"))

    return render_template("maintenance/detail.html", complaint=complaint)
