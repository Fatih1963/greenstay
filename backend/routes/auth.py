from flask import Blueprint, request, jsonify
from backend.models import User, db
from flask import current_app
import base64
import json
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Token functions
def encode_token(payload):
    """Simple token encoding"""
    payload['exp'] = (datetime.utcnow() + timedelta(days=7)).timestamp()
    json_payload = json.dumps(payload).encode('utf-8')
    encoded = base64.b64encode(json_payload).decode('utf-8')
    signature = base64.b64encode((encoded + current_app.config['SECRET_KEY']).encode('utf-8')).decode('utf-8')
    return f"{encoded}.{signature}"

def decode_token(token):
    """Simple token decoding"""
    try:
        encoded, signature = token.split('.')
        expected_signature = base64.b64encode((encoded + current_app.config['SECRET_KEY']).encode('utf-8')).decode('utf-8')
        if signature != expected_signature:
            return None
        json_payload = base64.b64decode(encoded).decode('utf-8')
        payload = json.loads(json_payload)
        if payload['exp'] < datetime.utcnow().timestamp():
            return None
        return payload
    except:
        return None

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                pass
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = decode_token(token)
            if not data:
                return jsonify({'message': 'Token is invalid!'}), 401
                
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User with this email already exists!'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken!'}), 409
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        is_host=data.get('is_host', False)
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully!', 'user': new_user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401
    
    token = encode_token({'user_id': user.id})
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    
    if 'username' in data and data['username'] != current_user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already taken!'}), 409
        current_user.username = data['username']
    
    if 'email' in data and data['email'] != current_user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already in use!'}), 409
        current_user.email = data['email']
    
    if 'password' in data:
        current_user.set_password(data['password'])
    
    if 'first_name' in data:
        current_user.first_name = data['first_name']
    
    if 'last_name' in data:
        current_user.last_name = data['last_name']
    
    if 'bio' in data:
        current_user.bio = data['bio']
    
    if 'profile_picture' in data:
        current_user.profile_picture = data['profile_picture']
    
    if 'phone_number' in data:
        current_user.phone_number = data['phone_number']
    
    if 'is_host' in data:
        current_user.is_host = data['is_host']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully!',
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logged out successfully!'}), 200
