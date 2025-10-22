FROM python:3.11-slim

WORKDIR /code

# Copy requirements from root
COPY requirements.txt /code/

# Copy all files from src/coursify-ai/
COPY src/coursify-ai/ /code/

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /code/pdfs /code/presentations /code/quiz_files

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Run main.py directly - NO wsgi.py needed!
CMD gunicorn main:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 300 --graceful-timeout 300 --preload