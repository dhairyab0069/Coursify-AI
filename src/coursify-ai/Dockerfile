FROM python:3.11-slim

WORKDIR /code

# Copy from build context root (Railway uses repo root as context)
COPY requirements.txt /code/
COPY src/coursify-ai/ /code/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Increased timeout and graceful timeout for Railway deployment
CMD gunicorn main:main --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 180 --graceful-timeout 180 --worker-class sync