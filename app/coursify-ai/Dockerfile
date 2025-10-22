FROM python:3.11-slim

WORKDIR /src

# Copy only the app/coursify-ai directory contents to /src
# This assumes build context is repo root
COPY app/coursify-ai /src

# Now /src directly contains app.py, requirements.txt, my_templates/, etc.
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Run gunicorn - now it will correctly find /src/app.py
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120