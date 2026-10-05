from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    if not User.query.filter_by(email="admin@hostel.com").first():
        admin = User(name="Hostel Admin", email="admin@hostel.com", role="admin")
        admin.set_password("Admin@123")
        db.session.add(admin)

    if not User.query.filter_by(email="staff@hostel.com").first():
        staff = User(name="Maintenance Staff", email="staff@hostel.com", role="maintenance")
        staff.set_password("Staff@123")
        db.session.add(staff)

    db.session.commit()
    print("Seed complete.")
    print("Admin: admin@hostel.com / Admin@123")
    print("Staff: staff@hostel.com / Staff@123")
