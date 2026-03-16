from flask import Blueprint, request, jsonify
from backend.models import Message, User, db
from backend.routes.auth import token_required

message_bp = Blueprint('messages', __name__)

@message_bp.route('', methods=['GET'])
@token_required
def get_messages(current_user):
    try:
        messages = Message.query.filter(
            (Message.receiver_id == current_user.id) | 
            (Message.sender_id == current_user.id)
        ).all()
        return jsonify([m.to_dict() for m in messages]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@message_bp.route('', methods=['POST'])
@token_required
def send_message(current_user):
    try:
        data = request.get_json()
        
        receiver = User.query.get(data.get('receiver_id'))
        if not receiver:
            return jsonify({'message': 'Receiver not found'}), 404
        
        new_message = Message(
            sender_id=current_user.id,
            receiver_id=data.get('receiver_id'),
            content=data.get('content')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({'message': 'Message sent', 'data': new_message.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@message_bp.route('/<int:message_id>/read', methods=['PUT'])
@token_required
def mark_as_read(current_user, message_id):
    try:
        message = Message.query.get(message_id)
        if not message:
            return jsonify({'message': 'Message not found'}), 404
        
        if message.receiver_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        message.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Message marked as read'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
