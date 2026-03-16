from flask import Blueprint, request, jsonify
from backend.models import Property, PropertyImage, db
from backend.routes.auth import token_required

property_bp = Blueprint('properties', __name__)

@property_bp.route('', methods=['GET'])
def get_properties():
    try:
        properties = Property.query.all()
        return jsonify([p.to_dict() for p in properties]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@property_bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    try:
        property = Property.query.get(property_id)
        if not property:
            return jsonify({'message': 'Property not found'}), 404
        return jsonify(property.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@property_bp.route('', methods=['POST'])
@token_required
def create_property(current_user):
    try:
        if not current_user.is_host:
            return jsonify({'message': 'Only hosts can create properties'}), 403
        
        data = request.get_json()
        
        new_property = Property(
            title=data.get('title'),
            description=data.get('description'),
            price_per_night=data.get('price_per_night'),
            location=data.get('location'),
            address=data.get('address'),
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            max_guests=data.get('max_guests'),
            property_type=data.get('property_type'),
            host_id=current_user.id,
            has_wifi=data.get('has_wifi', False),
            has_kitchen=data.get('has_kitchen', False),
            has_ac=data.get('has_ac', False),
            has_heating=data.get('has_heating', False),
            has_tv=data.get('has_tv', False),
            has_parking=data.get('has_parking', False),
            has_pool=data.get('has_pool', False)
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        return jsonify({'message': 'Property created', 'property': new_property.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@property_bp.route('/<int:property_id>', methods=['PUT'])
@token_required
def update_property(current_user, property_id):
    try:
        property = Property.query.get(property_id)
        if not property:
            return jsonify({'message': 'Property not found'}), 404
        
        if property.host_id != current_user.id:
            return jsonify({'message': 'You can only edit your own properties'}), 403
        
        data = request.get_json()
        
        if 'title' in data:
            property.title = data['title']
        if 'description' in data:
            property.description = data['description']
        if 'price_per_night' in data:
            property.price_per_night = data['price_per_night']
        if 'location' in data:
            property.location = data['location']
        if 'address' in data:
            property.address = data['address']
        if 'bedrooms' in data:
            property.bedrooms = data['bedrooms']
        if 'bathrooms' in data:
            property.bathrooms = data['bathrooms']
        if 'max_guests' in data:
            property.max_guests = data['max_guests']
        
        db.session.commit()
        return jsonify({'message': 'Property updated', 'property': property.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@property_bp.route('/<int:property_id>', methods=['DELETE'])
@token_required
def delete_property(current_user, property_id):
    try:
        property = Property.query.get(property_id)
        if not property:
            return jsonify({'message': 'Property not found'}), 404
        
        if property.host_id != current_user.id:
            return jsonify({'message': 'You can only delete your own properties'}), 403
        
        db.session.delete(property)
        db.session.commit()
        
        return jsonify({'message': 'Property deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
