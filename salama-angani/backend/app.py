from flask import Flask
from config import Config
from extensions import db, migrate, cors, jwt
from routes.flights import flights_bp
from routes.bookings import bookings_bp
from routes.auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app) # Initialize JWT manager

    # Register isolated route modules
    app.register_blueprint(flights_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(auth_bp) # Register Auth routes

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)