import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.models.user import db
from backend.routes.user import user_bp
from backend.routes.auth import auth_bp
from backend.routes.property import property_bp
from backend.routes.booking import booking_bp
from backend.routes.review import review_bp
from backend.routes.message import message_bp

# Create Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# CORS'u etkinleştir
CORS(app)

# SQLite veritabanı konfigürasyonu
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'airbnb.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    print(f"✓ Database initialized at {db_path}")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(property_bp, url_prefix='/api/properties')
app.register_blueprint(booking_bp, url_prefix='/api/bookings')
app.register_blueprint(review_bp, url_prefix='/api/reviews')
app.register_blueprint(message_bp, url_prefix='/api/messages')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    static_folder_path = app.static_folder
    if static_folder_path and os.path.exists(os.path.join(static_folder_path, 'index.html')):
        return send_from_directory(static_folder_path, 'index.html')
    return {'message': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'message': 'Internal server error'}, 500

# Serve static files (Multi-page HTML)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return {'message': 'Static folder not configured'}, 404

    # CSS, JS, images vs. statik dosyaları direkt serve et
    if path and os.path.isfile(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)

    # Sayfaları serve et
    page_map = {
        '': 'index.html',
        'index': 'index.html',
        'login': 'login.html',
        'register': 'register.html',
        'property': 'property.html',
        'bookings': 'bookings.html',
        'messages': 'messages.html',
    }

    # Path'ten sayfa adını belirle
    page_name = path.rstrip('/') if path else ''
    html_file = page_map.get(page_name, None)

    if html_file:
        html_path = os.path.join(static_folder_path, html_file)
        if os.path.exists(html_path):
            return send_from_directory(static_folder_path, html_file)

    # Eğer dosya bulunamazsa index.html döndür
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return {'message': 'index.html not found'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
