from app.extensions import db

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaints.id"), nullable=False, unique=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, server_default=db.func.now())
    completed_at = db.Column(db.DateTime)

    complaint = db.relationship("Complaint", back_populates="assignment")
    staff = db.relationship("User", foreign_keys=[staff_id], back_populates="assignments")
