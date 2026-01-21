# FastAPI Microservices (JWT + PostgreSQL)

Minimal template with two services: `auth-service` (JWT + Postgres) and `api-service` (token-protected).

Quick start (Docker)

1. Copy or edit the `.env` file and set a secure `SECRET_KEY` and DB credentials.
2. Build and start all services:

```bash
docker-compose up --build
```

- Traefik dashboard: http://localhost:8080
- Auth endpoints: http://auth.localhost/signup and http://auth.localhost/login
- API protected endpoint example: http://api.localhost/protected (use `Authorization: Bearer <token>`)

Run locally (optional)

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate
pip install -r auth-service/requirements.txt
pip install -r api-service/requirements.txt
docker-compose up -d db
# run auth service
cd auth-service\\app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# run api service (new shell)
cd ../../api-service/app
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Important environment variables (in `.env`)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`  database connection.
- `SECRET_KEY`  JWT signing key (replace for production).
- `AUTH_TOKEN_URL`  optional override for token verification URL used by the API service.

Production notes
- Do not store secrets in `.env` for productionuse Docker secrets or a secret manager.
- Use a strong, randomly generated `SECRET_KEY` and avoid committing it to source control.

Want to contribute or extend?
- Add tests for signup/login/verify flows.
- Add/maintain Alembic migrations under `auth-service/alembic/`.

See the `auth-service` and `api-service` folders for service-specific code and `requirements.txt` files.
