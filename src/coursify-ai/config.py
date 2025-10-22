import os
from datetime import timedelta

class Config:
    """Base configuration"""

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # MongoDB Configuration
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/coursify'
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'coursify')

    # LLM Provider Configuration
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'openai')  # 'openai', 'ollama', 'anthropic', etc.

    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')

    # Ollama Configuration (for local LLM)
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama2')

    # Generic LLM Configuration (backward compatibility)
    LLM_API_KEY = os.environ.get('OPENAI_API_KEY')  # Alias
    LLM_MODEL = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', '0.7'))
    LLM_MAX_TOKENS = int(os.environ.get('LLM_MAX_TOKENS', '2000'))

    # Anthropic Configuration (if you use Claude)
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

    # Flask Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

    # Session Configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per day, 50 per hour')

    # Email Configuration (if you use email)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@coursify.ai')

    # JWT Configuration (if you use JWT tokens)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Application Configuration
    APP_NAME = os.environ.get('APP_NAME', 'Coursify-AI')
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')

    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')

    # Cache Configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))

    # Celery Configuration (if you use background tasks)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

    # Ensure critical settings are configured in production
    @classmethod
    def validate(cls):
        """Validate that required production settings are configured"""
        required = ['SECRET_KEY', 'MONGODB_URI', 'OPENAI_API_KEY']
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required production config: {', '.join(missing)}")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    MONGODB_URI = 'mongodb://localhost:27017/coursify_test'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Get config based on environment
def get_config():
    """Get configuration based on FLASK_ENV environment variable"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])