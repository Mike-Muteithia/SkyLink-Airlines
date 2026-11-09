from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from models import Flight

flights_bp = Blueprint('flights', __name__, url_prefix='/api/flights')

# Public route: Anyone can view flights
@flights_bp.route('', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return jsonify([{
        'id': f.id,
        'flight_number': f.flight_number,
        'origin': f.origin,
        'destination': f.destination,
        'available_seats': f.available_seats,
        'base_price': f.base_price
    } for f in flights]), 200

# Protected route: Only 'providers' can add flights
@flights_bp.route('', methods=['POST'])
@jwt_required()
def create_flight():
    claims = get_jwt()
    # Check the custom role claim we embedded in the token during login
    if claims.get('role') != 'provider':
        return jsonify({'error': 'Unauthorized. Provider access required.'}), 403

    data = request.get_json()
    new_flight = Flight(
        flight_number=data['flight_number'],
        origin=data['origin'],
        destination=data['destination'],
        available_seats=data['available_seats'],
        base_price=data['base_price']
    )
    
    db.session.add(new_flight)
    db.session.commit()
    
    return jsonify({'message': 'Flight created successfully'}), 201