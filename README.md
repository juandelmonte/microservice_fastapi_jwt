# FastAPI Microservices with JWT Auth, PostgreSQL, Alembic, and Traefik

## Run the project
```bash
docker-compose up --build
```
- Traefik dashboard: http://localhost:8080

# FastAPI microservice template with JWT auth

Starter template for building small FastAPI microservices that use JWT for authentication and PostgreSQL for persistence. It's intended to be a minimal, working base you can fork or copy to start a new service.

Key features
- FastAPI-based services (separate `auth-service` and `api-service`).
- JWT authentication.
- PostgreSQL database for the auth service.
- Traefik reverse proxy.

Requirements
- Docker & Docker Compose
- Python 3.12 (only needed for local dev outside containers)

Quick start (Docker)
1. Copy or edit `.env` in the repo root and set a strong `SECRET_KEY` and DB values. A sample `.env` already exists with development defaults, but you should replace `SECRET_KEY` before using this in any real environment.

2. Build and run the services (recommended for local testing):

```powershell
docker-compose up --build
```

3. Services (local dev):
- Auth service: http://auth.localhost/signup and http://auth.localhost/login
- API service: http://api.localhost/protected (requires Authorization: Bearer <token>)
- Traefik dashboard: http://localhost:8080

Environment variables (in `.env`)
- POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST — DB connection details for the auth service.
- SECRET_KEY — the JWT signing key shared by auth-service and api-service.
- AUTH_TOKEN_URL (optional) — override the token URL used by the API service when verifying tokens.

Local development (without containers)
If you'd rather run the Python services locally (for debugging or faster iteration) you can install dependencies into a virtualenv and run uvicorn directly. The repo now includes `requirements.txt` for each service and the Dockerfiles install from those files as well.

Example (PowerShell):

```powershell
# create and activate virtualenv
python -m venv .venv
.\.venv\Scripts\Activate

# install each service's requirements
pip install -r auth-service/requirements.txt
pip install -r api-service/requirements.txt

# ensure .env is configured (set POSTGRES_HOST to a running Postgres instance)
# start Postgres via Docker Compose (just the DB) or run a local Postgres
docker-compose up -d db

# run auth service
cd auth-service\app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# in a new shell, run api service
cd api-service\app
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Notes:
- The Dockerfiles were updated to install dependencies from `requirements.txt` to match local development.
- When running services locally, point `POSTGRES_HOST` in `.env` to the DB (e.g. `localhost` or Docker host) and ensure credentials match.

Notes & recommendations
- The project uses `.env` for convenient local configuration. For production, use Docker secrets, a secret manager, or your platform's secret storage instead of a plain `.env` file.
- Replace the development `SECRET_KEY` with a securely generated random value (at least 32 bytes of entropy). Do not commit secrets to git.
- Consider removing fallback defaults in code for production so start-up fails if required environment variables are missing.

Suggested next steps
- Add automated tests for the auth flow (signup/login/verify).
- Add Alembic migration support (if you plan to evolve DB schemas).
- Replace `.env` usage with a secrets backend for deployments.

If you'd like, I can add a `requirements.txt` for local dev or implement a Docker-secrets example — tell me which you prefer.
