from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp
    from app.routes.maintenance import maintenance_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(maintenance_bp)

    with app.app_context():
        from app.models import User, Complaint, Assignment, Notification, Feedback
        db.create_all()

    return app
