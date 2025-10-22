# Use Python 3.11 instead of 3.9
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Test if app can be imported - this will show the actual error
RUN python -c "import sys; sys.path.insert(0, '.'); import app; print('✓ App imported successfully'); print('✓ Flask app:', app.app)" || (echo "✗ IMPORT FAILED - See error above" && exit 1)

# Run with gunicorn for production
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 --log-level debug --access-logfile - --error-logfile -
