import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from . import models, schemas

# Load environment variables from .env when running locally
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'username': db_user.username}

def login(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    token = jwt.encode({'sub': username}, SECRET_KEY, algorithm='HS256')
    return token