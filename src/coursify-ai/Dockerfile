FROM python:3.11-slim

WORKDIR /code

# Copy from relative to Dockerfile location (which is src/coursify-ai/)
COPY ../../requirements.txt /code/requirements.txt
COPY . /code/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

CMD gunicorn app:application --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120
