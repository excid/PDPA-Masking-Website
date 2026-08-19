# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ติดตั้ง dependency ก่อน copy source เพื่อให้ layer cache ทำงาน
COPY requirements.txt requirements-dev.txt ./

# ---------- dev image: มี pytest / ruff ----------
FROM base AS dev
RUN pip install -r requirements-dev.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---------- prod image: gunicorn + whitenoise ----------
FROM base AS prod
RUN pip install -r requirements.txt
COPY . .
RUN DJANGO_SECRET_KEY=build-only DJANGO_SETTINGS_MODULE=config.settings.prod \
    python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
