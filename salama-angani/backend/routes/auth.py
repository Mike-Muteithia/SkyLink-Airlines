from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Default to customer if no role is explicitly passed
    role = data.get('role', 'customer')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password for secure storage
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password, role=role)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Verify user exists and password matches the hash
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate a JWT containing the user ID and their specific role
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={'role': user.role}
    )
    
    return jsonify({
        'access_token': access_token, 
        'role': user.role,
        'email': user.email
    }), 200