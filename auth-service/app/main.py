from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import auth, models, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Auth Service")

@app.post('/signup')
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return auth.create_user(db, user)

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    token = auth.login(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return {'access_token': token, 'token_type': 'bearer'}