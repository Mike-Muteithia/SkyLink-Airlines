import os

class Config:
    # Defaults to local SQLite for WSL 2 testing
    db_url = os.getenv("DATABASE_URL", "sqlite:///salama_dev.db")
    
    # Fix Render's default postgres:// URI for modern SQLAlchemy compatibility
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add the secret key for token generation (defaults to a dev key if not in .env)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-development-key")