FROM python:3.11-slim

WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt /code/

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python modules
COPY *.py /code/

# Copy templates directory
COPY templates/ /code/templates/

# Create necessary directories
RUN mkdir -p /code/pdfs /code/presentations /code/quiz_files

EXPOSE 5000

# Environment variables
ENV FLASK_APP=wsgi.py
ENV PYTHONUNBUFFERED=1

# Run with gunicorn using wsgi.py
CMD gunicorn wsgi:application --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 300 --graceful-timeout 300 --preload