import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Complaint, Notification, Feedback

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.before_request
@login_required
def check_student():
    if current_user.role != "student":
        return redirect(url_for("auth.home"))

@student_bp.route("/dashboard")
def dashboard():
    complaints = Complaint.query.filter_by(student_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    counts = {
        "total": len(complaints),
        "pending": sum(c.status == "Pending" for c in complaints),
        "progress": sum(c.status == "In Progress" for c in complaints),
        "resolved": sum(c.status == "Resolved" for c in complaints),
        "closed": sum(c.status == "Closed" for c in complaints),
    }
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).all()
    return render_template("student/dashboard.html", complaints=complaints, counts=counts, notifications=notifications)

@student_bp.route("/complaints")
def complaints():
    items = Complaint.query.filter_by(student_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template("student/complaints.html", complaints=items)

@student_bp.route("/complaints/create", methods=["GET", "POST"])
def create_complaint():
    if request.method == "POST":
        image_name = None
        image = request.files.get("image")
        if image and image.filename:
            filename = secure_filename(image.filename)
            os.makedirs(os.path.join(current_app.root_path, "static", "uploads"), exist_ok=True)
            image.save(os.path.join(current_app.root_path, "static", "uploads", filename))
            image_name = filename

        complaint = Complaint(
            student_id=current_user.id,
            title=request.form["title"],
            description=request.form["description"],
            category=request.form["category"],
            priority=request.form["priority"],
            hostel=request.form.get("hostel"),
            room_number=request.form.get("room_number"),
            image=image_name
        )
        db.session.add(complaint)
        db.session.commit()

        flash("Complaint submitted successfully.", "success")
        return redirect(url_for("student.complaints"))

    return render_template("student/create_complaint.html")

@student_bp.route("/complaints/<int:complaint_id>")
def complaint_detail(complaint_id):
    complaint = Complaint.query.filter_by(id=complaint_id, student_id=current_user.id).first_or_404()
    return render_template("student/detail.html", complaint=complaint)

@student_bp.route("/complaints/<int:complaint_id>/feedback", methods=["POST"])
def feedback(complaint_id):
    complaint = Complaint.query.filter_by(id=complaint_id, student_id=current_user.id).first_or_404()
    if complaint.status != "Resolved":
        flash("Feedback is available after resolution.", "warning")
        return redirect(url_for("student.complaint_detail", complaint_id=complaint.id))

    if complaint.feedback:
        flash("Feedback already submitted.", "warning")
        return redirect(url_for("student.complaint_detail", complaint_id=complaint.id))

    rating = int(request.form["rating"])
    rating = max(1, min(5, rating))
    fb = Feedback(complaint_id=complaint.id, student_id=current_user.id, rating=rating, comment=request.form.get("comment"))
    complaint.status = "Closed"
    db.session.add(fb)
    db.session.commit()
    flash("Thank you for your feedback.", "success")
    return redirect(url_for("student.complaint_detail", complaint_id=complaint.id))

@student_bp.route("/notifications/<int:notification_id>/read")
def read_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return redirect(url_for("student.dashboard"))
