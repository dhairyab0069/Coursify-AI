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

# MongoDB will be initialized in main.py with config
mongo_client = None
db = None
fs = None
users_collection = None
reviews_collection = None
serializer = None


def init_mongodb(app):
    """Initialize MongoDB connection"""
    global mongo_client, db, fs, users_collection, reviews_collection, serializer

    from config import Config

    # Create MongoDB client
    mongo_uri = Config.MONGODB_URI or Config.MONGO_URL
    mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)

    # Test connection
    try:
        mongo_client.server_info()
        print("✓ Successfully connected to MongoDB!")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise

    # Use ONE database with multiple collections
    db = mongo_client[Config.MONGODB_DB_NAME]

    # Initialize GridFS for file storage
    fs = GridFS(db)

    # Initialize collections
    users_collection = db.users
    reviews_collection = db.reviews

    # Serializer for tokens
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    print(f"✓ MongoDB collections initialized: users, reviews")

    return mongo_client