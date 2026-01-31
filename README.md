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
- `CORS_ORIGINS`  comma-separated list of allowed origins (default: `http://localhost:3000` for React dev server).
- `ACCESS_TOKEN_EXPIRE_MINUTES`  access token lifetime in minutes (default: 15).
- `REFRESH_TOKEN_EXPIRE_DAYS`  refresh token lifetime in days (default: 7).

React Integration

### What Changed (for React support)
- ✅ CORS middleware enabled on both services
- ✅ Login endpoint now returns `access_token`, `refresh_token`, and `expires_in`
- ✅ New `/refresh` endpoint to get a new access token using refresh token

### React Client Example

```javascript
// auth.js - Handle authentication
const API_URL = 'http://auth.localhost';
const API_SERVICE_URL = 'http://api.localhost';

export async function login(username, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }),
    credentials: 'include'
  });
  
  if (!response.ok) throw new Error('Login failed');
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('expires_in', Date.now() + data.expires_in * 1000);
  
  return data;
}

export async function refreshAccessToken() {
  const refresh_token = localStorage.getItem('refresh_token');
  
  const response = await fetch(`${API_URL}/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token }),
    credentials: 'include'
  });
  
  if (!response.ok) {
    localStorage.clear();
    throw new Error('Session expired');
  }
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('expires_in', Date.now() + data.expires_in * 1000);
  
  return data;
}

export async function callProtectedAPI(endpoint) {
  let token = localStorage.getItem('access_token');
  const expiresIn = localStorage.getItem('expires_in');
  
  // Refresh if expired
  if (Date.now() >= expiresIn) {
    await refreshAccessToken();
    token = localStorage.getItem('access_token');
  }
  
  const response = await fetch(`${API_SERVICE_URL}${endpoint}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });
  
  if (response.status === 401) {
    await refreshAccessToken();
    token = localStorage.getItem('access_token');
    return fetch(`${API_SERVICE_URL}${endpoint}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    });
  }
  
  return response.json();
}

export function logout() {
  localStorage.clear();
}
```

### Usage in React Component

```javascript
import { login, logout, callProtectedAPI } from './auth';

function App() {
  const handleLogin = async () => {
    await login('testuser', 'password123');
    const data = await callProtectedAPI('/protected');
    console.log(data);
  };
  
  const handleLogout = () => logout();
  
  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
```

Production notes
- Do not store secrets in `.env` for productionuse Docker secrets or a secret manager.
- Use a strong, randomly generated `SECRET_KEY` and avoid committing it to source control.

Want to contribute or extend?
- Add tests for signup/login/verify flows.
- Add/maintain Alembic migrations under `auth-service/alembic/`.

See the `auth-service` and `api-service` folders for service-specific code and `requirements.txt` files.
