FROM python:3.11-slim

WORKDIR /code

# Copy requirements from root
COPY requirements.txt /code/

# Copy all files from src/coursify-ai/
COPY src/coursify-ai/ /code/

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories for generated content
RUN mkdir -p /code/pdfs /code/presentations /code/quiz_files

EXPOSE 5000

ENV FLASK_APP=wsgi.py
ENV PYTHONUNBUFFERED=1

# Run with gunicorn
CMD gunicorn wsgi:application --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 300 --graceful-timeout 300 --preload