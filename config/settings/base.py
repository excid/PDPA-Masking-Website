"""ค่าตั้งที่ใช้ร่วมกันทั้ง dev และ prod."""
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, []),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-insecure-change-me")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "masking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

# โปรเจกต์นี้ไม่เก็บข้อมูลผู้ใช้ลง DB (ตามหลัก PDPA — ไม่เก็บคือปลอดภัยที่สุด)
# ถ้าภายหลังต้องใช้ ค่อยเปิด DATABASES + django.contrib.auth
DATABASES: dict = {}

LANGUAGE_CODE = "th"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---- ค่าเฉพาะของโปรเจกต์ ----
# จำกัดขนาดข้อความที่รับ เพื่อกัน regex ทำงานนานเกินไป
MASKING_MAX_INPUT_CHARS = 20_000

# ลิงก์ GitHub ที่โจทย์บังคับให้แสดงบนหน้าเว็บ
GITHUB_REPO_URL = env(
    "GITHUB_REPO_URL", default="https://github.com/excid/pdpa-masking-website"
)
