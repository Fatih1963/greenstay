# GreenStay - Vacation Rental Platform

A lightweight vacation rental booking platform built with Flask and SQLite. Browse properties, make reservations, leave reviews, and connect with hosts.

**GreenStay** is an Airbnb-like platform perfect for learning full-stack web development. Built entirely with SQLite - no database server setup needed.

## Live Demo

[http://localhost:5000](http://localhost:5000)

## Features

- User authentication with token-based system
- Browse property listings with detailed information
- Make and manage reservations
- Leave reviews and ratings for properties
- Real-time messaging between guests and hosts
- Host and guest role management
- Responsive design with modern UI
- Built-in SQLite database - zero setup required

## Requirements

- Python 3.12+ (Python 3.13 has SQLAlchemy compatibility issues)
- pip (Python package manager)
- SQLite3 (included with Python)

**IMPORTANT**: This project was built with Python 3.12. SQLAlchemy 2.0.23 has compatibility issues with Python 3.13. Use Python 3.12 or earlier.

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/fatih1963/greenstay.git
cd greenstay
```

### 2. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

### 5. Start Backend Server
```bash
cd backend
python main.py
```

### 6. Open in Browser
```
http://localhost:5000
```

## Project Structure

```
greenstay/
├── backend/
│   ├── main.py              # Flask application entry point
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py          # User model
│   │   ├── property.py      # Property listings
│   │   ├── booking.py       # Reservations
│   │   ├── review.py        # Reviews & ratings
│   │   └── message.py       # Messaging
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── property.py      # Property operations
│   │   ├── booking.py       # Booking management
│   │   ├── review.py        # Review system
│   │   └── message.py       # Messaging
│   └── static/              # Frontend HTML, CSS, JS
├── database/
│   └── airbnb.db           # Auto-generated SQLite DB
├── frontend/                # Original frontend source files
│   ├── html/
│   ├── css/
│   └── js/
├── requirements.txt
├── .env.example
└── README.md
```

## API Documentation

### Authentication Endpoints
```
POST   /api/auth/register      # Create new account
POST   /api/auth/login         # Login & get token
GET    /api/auth/profile       # Get user profile (requires token)
PUT    /api/auth/profile       # Update profile (requires token)
POST   /api/auth/logout        # Logout (requires token)
```

### Property Endpoints
```
GET    /api/properties              # List all properties
GET    /api/properties/<id>         # Get property details
POST   /api/properties              # Create new property (host only)
PUT    /api/properties/<id>         # Edit property (host only)
DELETE /api/properties/<id>         # Delete property (host only)
```

### Booking Endpoints
```
GET    /api/bookings                # List user bookings (requires token)
GET    /api/bookings/<id>           # Get booking details (requires token)
POST   /api/bookings                # Create booking (requires token)
DELETE /api/bookings/<id>           # Cancel booking (requires token)
```

### Review Endpoints
```
GET    /api/reviews/property/<id>   # Get property reviews
POST   /api/reviews                 # Leave a review (requires token)
DELETE /api/reviews/<id>            # Delete review (requires token)
```

### Messaging Endpoints
```
GET    /api/messages                # Get conversations (requires token)
POST   /api/messages                # Send message (requires token)
PUT    /api/messages/<id>/read      # Mark as read (requires token)
```

### User Endpoints
```
GET    /api/users                   # List all users
GET    /api/users/<id>              # Get user profile
```

## Database

SQLite database is automatically created at `database/airbnb.db` on first run.

### Reset Database
```bash
rm database/airbnb.db
# Restart backend - new database will be created automatically
```

## Testing the API

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler",
    "email": "traveler@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "traveler@example.com",
    "password": "securepass123"
  }'
```

### Get Profile (requires token)
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Browse Properties
```bash
curl http://localhost:5000/api/properties
```

## Troubleshooting

### Python 3.13 Compatibility Error
If you get `AssertionError: Class directly inherits TypingOnly`, you're using Python 3.13.

**Solution**: Downgrade to Python 3.12
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port 5000 Already in Use
Edit `backend/main.py` and change the port:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### Module Import Error
Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues
Reset the database:
```bash
rm database/airbnb.db
python main.py  # Will recreate database
```

## Technologies Used

- **Backend Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Authentication**: Token-based (base64 encoded)
- **API**: RESTful endpoints with CORS support

## File Sizes

- Lightweight codebase: ~50KB Python code
- SQLite database: Starts at ~1MB
- No external services required

## Development

### Add a New Python Package
```bash
pip install package_name
pip freeze > requirements.txt
```

### Deploy Frontend to Backend
```bash
mkdir -p backend/static/css backend/static/js
cp frontend/html/* backend/static/
cp -r frontend/css backend/static/
cp -r frontend/js backend/static/
```

### Run with Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

MIT License - See LICENSE file for details

## Author

**Fatih Kaya**
- GitHub: [@fatih1963](https://github.com/fatih1963)
- Project: [GreenStay](https://github.com/fatih1963/greenstay)

## Roadmap

- [ ] Image upload for properties
- [ ] Payment integration (Stripe/PayPal)
- [ ] Advanced search filters
- [ ] Map view with Leaflet.js
- [ ] User reviews with photos
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Mobile app (Flutter/React Native)

## Learning Resources

This project demonstrates:
- Flask web framework
- SQLAlchemy ORM
- RESTful API design
- Token-based authentication
- Database design with SQLite
- Frontend-backend communication
- HTML/CSS/JavaScript

Perfect for students learning:
- Full-stack web development
- Python backend development
- REST API creation
- Database management
- Web authentication

## Support

Found a bug? Need help?
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## Related Projects

Similar projects for learning:
- Django Blog Platform
- FastAPI Todo Application
- Node.js E-commerce Site

---

**GreenStay** - Built with Python 3.12 + SQLite. No database server needed. Perfect for learning full-stack development.

Happy coding! 
