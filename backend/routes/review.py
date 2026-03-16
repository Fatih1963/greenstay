from flask import Blueprint, request, jsonify
from backend.models import Review, Property, db
from backend.routes.auth import token_required

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/property/<int:property_id>', methods=['GET'])
def get_property_reviews(property_id):
    try:
        reviews = Review.query.filter_by(property_id=property_id).all()
        return jsonify([r.to_dict() for r in reviews]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@review_bp.route('', methods=['POST'])
@token_required
def create_review(current_user):
    try:
        data = request.get_json()
        
        property = Property.query.get(data.get('property_id'))
        if not property:
            return jsonify({'message': 'Property not found'}), 404
        
        new_review = Review(
            property_id=data.get('property_id'),
            guest_id=current_user.id,
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({'message': 'Review created', 'review': new_review.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@review_bp.route('/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, review_id):
    try:
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'message': 'Review not found'}), 404
        
        if review.guest_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
