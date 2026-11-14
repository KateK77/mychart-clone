import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv("CC_PRODUCTION") != "1"
SECRET_KEY = os.environ["CC_SECRET_KEY"] if not DEBUG else os.getenv("CC_SECRET_KEY", "careconnect-local-synthetic-only")
ALLOWED_HOSTS = os.getenv("CC_HOSTS", "localhost,127.0.0.1,testserver").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CC_TRUSTED_ORIGINS", "http://localhost:15260,http://127.0.0.1:15260").split(",")
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "rest_framework", "portal",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "careconnect.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True,
              "OPTIONS": {"context_processors": ["django.template.context_processors.request",
                 "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.getenv("CC_SQLITE", BASE_DIR / "db.sqlite3"), "OPTIONS": {"timeout": 20, "transaction_mode": "IMMEDIATE"}}}
if not DEBUG or os.getenv("CC_DB_NAME"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql", "NAME": os.environ["CC_DB_NAME"],
        "USER": os.environ["CC_DB_USER"], "PASSWORD": os.environ["CC_DB_PASSWORD"],
        "HOST": os.getenv("CC_DB_HOST", "localhost"), "PORT": os.getenv("CC_DB_PORT", "5432"),
    }
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{name}"}
    for name in ("UserAttributeSimilarityValidator", "MinimumLengthValidator",
                 "CommonPasswordValidator", "NumericPasswordValidator")
]
USE_TZ = True
TIME_ZONE = "UTC"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_AGE = 60 * 60 * 8
SECURE_CONTENT_TYPE_NOSNIFF = True
REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
                  "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"]}

# Each local version uses separate cookies, so signing into v2 cannot change v1 sessions.
SESSION_COOKIE_NAME = os.getenv("CC_SESSION_COOKIE", "careconnect_v2_session")
CSRF_COOKIE_NAME = "csrftoken_v2"
DEMO_MAILBOX = DEBUG and os.getenv("CC_DEMO_MAILBOX", "1") == "1"
REST_FRAMEWORK["EXCEPTION_HANDLER"] = "portal.errors.portal_exception_handler"
