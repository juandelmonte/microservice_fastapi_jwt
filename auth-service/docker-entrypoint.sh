#!/bin/sh
set -e

echo "Waiting for DB to be available..."
# Retry loop using psycopg2 (psycopg2 is installed in the image)
python - <<'PY'
import time, os
import psycopg2

host = os.environ.get('POSTGRES_HOST', 'db')
user = os.environ.get('POSTGRES_USER', 'postgres')
password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
dbname = os.environ.get('POSTGRES_DB', 'authdb')

while True:
    try:
        conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
        conn.close()
        print('Postgres is available')
        break
    except Exception:
        print('Waiting for postgres...')
        time.sleep(1)
PY

echo "Running DB migrations..."
alembic upgrade head

echo "Starting server: $@"
exec "$@"
