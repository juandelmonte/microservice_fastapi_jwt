FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies from requirements.txt for better caching and local dev parity
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy migrations and entrypoint script so container can run migrations on start
COPY alembic.ini ./
COPY alembic ./alembic
COPY docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

COPY ./app /app

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]