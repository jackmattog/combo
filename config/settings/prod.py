import os
from .base import *

# 1. CORE OVERRIDES
# SECURITY WARNING: absolutely do not run with debug turned on in production!
DEBUG = False

# Fails loudly if the environment variable is missing
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Only allow your actual domains
ALLOWED_HOSTS = [
    "api.yourdomain.com", 
    "yourdomain.com",
    "192.168.1.100", # Example Server IP
]

# 2. DATABASE CONFIGURATION
# Assuming PostgreSQL. Read credentials from the server environment.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "my_prod_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ["DB_PASSWORD"], # Will throw an error if missing
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# 3. CORS SETTINGS
# Only allow your production frontend to hit the API
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# 4. HTTPS & SECURITY HEADERS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 Year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 5. DRF PRODUCTION OVERRIDES
# Disable the browsable API in production to save resources and hide API structures
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
]

# 6. STATIC FILES (Optional but recommended)
# If serving static files directly from Django (e.g., via WhiteNoise)
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 7. LOGGING
# Catch errors and output them to the console (useful for Docker/Heroku/Render)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}