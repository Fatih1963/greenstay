from datetime import datetime
from backend.models.user import db

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_kitchen = db.Column(db.Boolean, default=False)
    has_ac = db.Column(db.Boolean, default=False)
    has_heating = db.Column(db.Boolean, default=False)
    has_tv = db.Column(db.Boolean, default=False)
    has_parking = db.Column(db.Boolean, default=False)
    has_pool = db.Column(db.Boolean, default=False)
    property_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key relationships
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    host = db.relationship('User', backref=db.backref('properties', lazy=True))
    
    # Relationships
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship('Booking', backref='property', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='property', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Property {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'location': self.location,
            'address': self.address,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'max_guests': self.max_guests,
            'has_wifi': self.has_wifi,
            'has_kitchen': self.has_kitchen,
            'has_ac': self.has_ac,
            'has_heating': self.has_heating,
            'has_tv': self.has_tv,
            'has_parking': self.has_parking,
            'has_pool': self.has_pool,
            'property_type': self.property_type,
            'host_id': self.host_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'images': [image.to_dict() for image in self.images],
            'average_rating': self.get_average_rating()
        }
    
    def get_average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PropertyImage {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'property_id': self.property_id,
            'created_at': self.created_at.isoformat()
        }
