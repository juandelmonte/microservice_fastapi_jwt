import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import jwt
from fastapi import HTTPException
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env when running locally
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed = pwd_context.hash(user.password)
    except ValueError as e:
        # Defensive: passlib/bcrypt can raise ValueError for passwords >72 bytes
        # Log the exception detail to help debugging why hashing failed.
        logger.exception("bcrypt hashing failed: %s", e)
        raise HTTPException(status_code=400, detail='Password too long for bcrypt (max 72 bytes).')

    db_user = models.User(username=user.username, password=hashed)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # username already exists (unique constraint) — surface a 400 instead of 500
        raise HTTPException(status_code=400, detail='username already exists')
    db.refresh(db_user)
    return {'username': db_user.username}

def login(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    try:
        ok = pwd_context.verify(password, user.password)
    except ValueError:
        # verify can raise ValueError if password too long for bcrypt — treat as invalid credentials
        return None
    if not ok:
        return None
    token = jwt.encode({'sub': username}, SECRET_KEY, algorithm='HS256')
    return token