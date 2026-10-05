from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Complaint, Assignment, Notification

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.home"))
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    staff = User.query.filter_by(role="maintenance").all()
    stats = {
        "total": len(complaints),
        "pending": sum(c.status == "Pending" for c in complaints),
        "assigned": sum(c.status == "Assigned" for c in complaints),
        "progress": sum(c.status == "In Progress" for c in complaints),
        "resolved": sum(c.status == "Resolved" for c in complaints),
        "closed": sum(c.status == "Closed" for c in complaints),
    }
    return render_template("admin/dashboard.html", complaints=complaints, staff=staff, stats=stats)

@admin_bp.route("/complaints/<int:complaint_id>", methods=["GET", "POST"])
@admin_required
def complaint_detail(complaint_id):
    complaint = db.get_or_404(Complaint, complaint_id)
    staff = User.query.filter_by(role="maintenance").all()

    if request.method == "POST":
        staff_id = int(request.form["staff_id"])
        assignment = Assignment.query.filter_by(complaint_id=complaint.id).first()
        if not assignment:
            assignment = Assignment(complaint_id=complaint.id, staff_id=staff_id, assigned_by=current_user.id)
            db.session.add(assignment)
        else:
            assignment.staff_id = staff_id

        complaint.status = "Assigned"
        db.session.add(Notification(user_id=staff_id, message=f"Complaint #{complaint.id} has been assigned to you."))
        db.session.commit()
        flash("Complaint assigned successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/detail.html", complaint=complaint, staff=staff)
