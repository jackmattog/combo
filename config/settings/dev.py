# Import everything from base.py
from .base import * # 1. CORE OVERRIDES
# debug true in production
DEBUG = True

# secret key for local development only
SECRET_KEY = "django-insecure-dummy-key-for-local-dev-only"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 2. DATABASE CONFIGURATION
# Using SQLite locally for fast setup. 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 3. CORS SETTINGS (For separate local frontends)
# This allow local frontend servers to make API requests
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",   # Default React port
    "http://localhost:5173",   # Default Vite/Vue port
    "http://127.0.0.1:5500",   # Default VSCode Live Server port
]

# 4. EMAIL SETTINGS
# Print emails to the terminal console instead of sending them via SMTP
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# If locked down the API in base.py, this might used to add the 
# Browsable API back in for easy local testing.
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer", # Provides the DRF web UI
]
