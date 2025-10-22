# Use Python 3.11 instead of 3.9
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY . /src

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Diagnostic: Show file structure and what's in the app module
RUN echo "=== Files in /app ===" && ls -la /app && \
    echo "=== Checking for app.py ===" && test -f /app/app.py && echo "✓ app.py exists" || echo "✗ app.py NOT FOUND" && \
    echo "=== Checking for app/ directory ===" && test -d /app/app && echo "⚠ app/ directory exists (CONFLICT!)" || echo "✓ No app/ directory" && \
    echo "=== What Python sees when importing 'app' ===" && \
    python -c "import sys; sys.path.insert(0, '.'); import app; print('Module location:', app.__file__); print('Module type:', type(app)); print('Has app attr?', hasattr(app, 'app')); import inspect; print('First 50 lines of app.py:'); print(inspect.getsource(app)[:2000])" || echo "Import failed"

# Run with gunicorn for production
CMD gunicorn app:application --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120

