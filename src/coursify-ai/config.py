import os
from datetime import timedelta

class Config:
    """Base configuration"""

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # MongoDB Configuration
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/coursify'

    # OpenAI/LLM Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'openai')  # Default to 'openai'
    LLM_MODEL = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')  # Default model
    LLM_API_KEY = os.environ.get('OPENAI_API_KEY')  # Alias for compatibility

    # Flask Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False

    # Session Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # CORS Configuration (if needed)
    CORS_HEADERS = 'Content-Type'

    # File Upload Configuration (if you handle file uploads)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Rate Limiting (optional)
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}