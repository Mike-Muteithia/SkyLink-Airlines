from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # 'customer' or 'provider'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Establish relationship to bookings
    bookings = db.relationship('Booking', backref='owner', lazy=True)

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(8), unique=True, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Links to User
    passenger_name = db.Column(db.String(100), nullable=False)