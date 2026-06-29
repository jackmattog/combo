from pathlib import Path

# .parent.parent.parent points to: config ./
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 2. APP CONFIGURATION
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]

LOCAL_APPS = [
    # Project apps
    "apps.lesotho.bar_orders",
    "apps.lesotho.bar_products",
    "apps.lesotho.lesotho_carwash",
    "apps.lesotho.lodge_rooms",
    "apps.mpc.mpc_orders",
    "apps.mpc.mpc_products",
    "apps.shared.accounts",
    "apps.shared.core",
    "apps.shared.suggestions",
    "apps.upmatt.upmatt_softwares",
    "apps.upmatt.web_services",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# 3. MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be as high as possible
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"  # If using Channels/Async

# 4. DJANGO REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # Default Authentication: How users identify themselves
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework_simplejwt.authentication.JWTAuthentication", # Common for APIs
        "rest_framework.authentication.SessionAuthentication",
    ],
    # Pagination: Prevent heavy queries from crashing your API
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    # Exception Handling: Optional, custom handler if needed
    # "EXCEPTION_HANDLER": "config.utils.custom_exception_handler",
}

# 5. TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 6. INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 7. STATIC & MEDIA FILES
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# 8. DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"