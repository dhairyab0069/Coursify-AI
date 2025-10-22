"""
User model for Flask-Login
"""
from flask_login import UserMixin
from bson.objectid import ObjectId
from extensions import users_collection


class User(UserMixin):
    """User class for Flask-Login"""

    def __init__(self, user_id, email):
        self.user_id = str(user_id)
        self.email = email

    def get_id(self):
        return self.user_id


def load_user(user_id):
    """Load user from database"""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(user_id=user["_id"], email=user["email"])