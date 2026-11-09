from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash
from flask_migrate import upgrade
from sqlalchemy import text

with app.app_context():
    # 1. Forcefully wipe the PostgreSQL public schema at the database level
    db.session.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    db.session.commit()
    
    # 2. Run the Alembic migrations to build the new tables cleanly
    upgrade()
    
    # 3. Seed the production admin account
    if not User.query.filter_by(email='admin@salama.com').first():
        provider = User(
            email='admin@salama.com', 
            password_hash=generate_password_hash('admin123'), 
            role='provider'
        )
        db.session.add(provider)
        db.session.commit()
        print("Production database forcefully reset, migrated, and seeded successfully!")