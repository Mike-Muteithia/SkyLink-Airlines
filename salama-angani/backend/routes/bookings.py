import time
import uuid
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import Booking, Flight
from utils import generate_pdf_ticket

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    flight = Flight.query.get_or_404(data.get('flight_id'))
    
    if flight.available_seats <= 0:
        return jsonify({'error': 'Flight fully booked'}), 400

    # Simulate payment gateway processing latency
    time.sleep(2)

    flight.available_seats -= 1
    pnr = str(uuid.uuid4())[:8].upper()
    
    new_booking = Booking(
        booking_reference=pnr, 
        flight_id=flight.id, 
        user_id=current_user_id, 
        passenger_name=data.get('passenger_name')
    )
    
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'booking_reference': pnr, 'status': 'SUCCESS'}), 201

@bookings_bp.route('/<pnr>/ticket', methods=['GET'])
@jwt_required()
def download_ticket(pnr):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    booking = Booking.query.filter_by(booking_reference=pnr).first_or_404()
    
    # Security: Ensure only the ticket owner (or a provider) can download this PDF
    if claims.get('role') != 'provider' and str(booking.user_id) != str(current_user_id):
        return jsonify({'error': 'Unauthorized access to ticket'}), 403

    flight = Flight.query.get(booking.flight_id)
    pdf_buffer = generate_pdf_ticket(booking, flight)
    
    return send_file(
        pdf_buffer, 
        as_attachment=True, 
        download_name=f"Salama_Angani_Ticket_{pnr}.pdf", 
        mimetype='application/pdf'
    )

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_my_bookings():
    current_user_id = get_jwt_identity()
    
    # Fetch all bookings for the logged-in user and join the flight details
    user_bookings = db.session.query(Booking, Flight).join(Flight).filter(Booking.user_id == current_user_id).all()
    
    result = []
    for booking, flight in user_bookings:
        result.append({
            'pnr': booking.booking_reference,
            'passenger_name': booking.passenger_name,
            'flight_number': flight.flight_number,
            'origin': flight.origin,
            'destination': flight.destination,
            'price': flight.base_price
        })
        
    return jsonify(result), 200