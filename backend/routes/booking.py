from flask import Blueprint, request, jsonify
from backend.models import Booking, Property, db
from backend.routes.auth import token_required

booking_bp = Blueprint('bookings', __name__)

@booking_bp.route('', methods=['GET'])
@token_required
def get_bookings(current_user):
    try:
        bookings = Booking.query.filter_by(guest_id=current_user.id).all()
        return jsonify([b.to_dict() for b in bookings]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@token_required
def get_booking(current_user, booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.guest_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        return jsonify(booking.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@booking_bp.route('', methods=['POST'])
@token_required
def create_booking(current_user):
    try:
        data = request.get_json()
        
        property = Property.query.get(data.get('property_id'))
        if not property:
            return jsonify({'message': 'Property not found'}), 404
        
        new_booking = Booking(
            property_id=data.get('property_id'),
            guest_id=current_user.id,
            check_in=data.get('check_in'),
            check_out=data.get('check_out'),
            number_of_guests=data.get('number_of_guests'),
            total_price=data.get('total_price'),
            status='confirmed'
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({'message': 'Booking created', 'booking': new_booking.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@token_required
def cancel_booking(current_user, booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.guest_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        booking.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'message': 'Booking cancelled'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
