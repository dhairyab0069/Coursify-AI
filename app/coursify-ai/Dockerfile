FROM python:3.11-slim

WORKDIR /src

# Copy requirements.txt from repo root
COPY requirements.txt /src/

# Copy the coursify-ai app contents
COPY app/coursify-ai /src/

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Run gunicorn
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120