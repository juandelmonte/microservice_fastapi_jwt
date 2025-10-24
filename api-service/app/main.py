from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import jwt

# Load environment variables (supports running locally with a .env file)
load_dotenv()

TOKEN_URL = os.getenv('AUTH_TOKEN_URL', 'http://auth-service:8000/login')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

app = FastAPI(title='API Service')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('sub')
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')


@app.get('/protected')
def protected_route(user: str = Depends(get_current_user)):
    return {'message': f'Hello {user}, you are authorized!'}