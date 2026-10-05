from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="student")
    hostel = db.Column(db.String(100))
    room_number = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    complaints = db.relationship("Complaint", back_populates="student", foreign_keys="Complaint.student_id")
    assignments = db.relationship("Assignment", back_populates="staff", foreign_keys="Assignment.staff_id")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_staff(self):
        return self.role == "maintenance"
