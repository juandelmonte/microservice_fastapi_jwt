from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import auth, models, database, schemas
import os
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Auth Service")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:3000","http://api.localhost","http://auth.localhost"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/signup')
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return auth.create_user(db, user)

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    result = auth.login(db, form_data.username, form_data.password)
    if not result:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return result

@app.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(
    body: schemas.RefreshTokenRequest,
    db: Session = Depends(database.get_db)
):
    # Extract token
    refresh_token_str = body.refresh_token

    # Generate new tokens
    result = auth.refresh_access_token(refresh_token_str)
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    return result

@app.post("/test2")
def test(body: schemas.RefreshTokenRequest):
    return body

