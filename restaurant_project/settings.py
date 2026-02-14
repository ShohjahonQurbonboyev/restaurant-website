import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-replace-with-your-secret-key"
DEBUG = True

# ✅ dev uchun
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "jazzmin",  # ✅ har doim admin'dan oldin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "restaurant_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "restaurant_project.urls"


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

                "restaurant_app.context_processors.cart_count",
            ],

            
            
        },
    },
]


WSGI_APPLICATION = "restaurant_project.wsgi.application"

# ---------- PostgreSQL ----------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "restaurant",
        "USER": "postgres",
        "PASSWORD": "998974744114",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# ---------- Password validators ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# ✅ Static / Media
STATIC_URL = "/static/"

# ✅ devda static qayerdan olinadi:
# Eslatma: admin/jazzmin staticlari o‘z app’laridan avtomatik topiladi,
# bu esa faqat sizning project staticlaringiz uchun.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ✅ productionda collectstatic chiqadigan joy (hozir ham bo‘lsa zarar qilmaydi)
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- Jazzmin ----------
JAZZMIN_SETTINGS = {
    "site_title": "Restaurant Admin",
    "site_header": "Restaurant Dashboard",
    "site_brand": "My Restaurant",
    "welcome_sign": "Admin panelga xush kelibsiz!",
    "copyright": "My Restaurant",
    "search_model": ["restaurant_app.MenuItem", "restaurant_app.Order"],

    "topmenu_links": [
        {"name": "Sayt", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "restaurant_app.MenuItem": "fas fa-utensils",
        "restaurant_app.Order": "fas fa-receipt",
        "restaurant_app.OrderItem": "fas fa-list",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": True,

    # ✅ tablar
    "changeform_format": "single",
}

# Optional: Stripe
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
