"""
Flask extensions initialization
"""
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient
from gridfs import GridFS
from itsdangerous import URLSafeTimedSerializer

# Initialize extensions
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()

# MongoDB will be initialized in app.py with config
mongo_client = None
db = None
db_users = None
db_reviews = None
fs = None
users_collection = None
reviews_collection = None
serializer = None


def init_mongodb(app):
    """Initialize MongoDB connection"""
    global mongo_client, db, db_users, db_reviews, fs, users_collection, reviews_collection, serializer

    from config import Config

    # Create MongoDB client
    mongo_client = MongoClient(Config.MONGO_URL, serverSelectionTimeoutMS=10000)

    # Test connection
    try:
        mongo_client.server_info()
        print("✓ Successfully connected to MongoDB!")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise

    # Database references
    db = mongo_client[Config.DB_PDFS]
    db_users = mongo_client[Config.DB_USERS]
    db_reviews = mongo_client[Config.DB_REVIEWS]
    fs = GridFS(db)
    users_collection = db_users.users
    reviews_collection = db_reviews.reviews

    # Serializer for tokens
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    return mongo_client