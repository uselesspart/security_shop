#!/usr/bin/env bash
set -e

echo "Waiting for Postgres ${DB_HOST}:${DB_PORT:-5432}..."

python <<'PY'
import os, time, psycopg2
while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "postgres"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "postgres"),
            host=os.environ.get("DB_HOST", "pgdb"),
            port=os.environ.get("DB_PORT", "5432"),
        )
        conn.close()
        break
    except Exception as e:
        print("DB not ready:", e)
        time.sleep(1)
PY

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput 

echo "Starting server..."
exec "$@"