from app.extensions import db

class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    status = db.Column(db.String(30), nullable=False, default="Pending")
    hostel = db.Column(db.String(100))
    room_number = db.Column(db.String(30))
    image = db.Column(db.String(255))
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    student = db.relationship("User", back_populates="complaints", foreign_keys=[student_id])
    assignment = db.relationship("Assignment", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    feedback = db.relationship("Feedback", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
