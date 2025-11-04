FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static media

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]