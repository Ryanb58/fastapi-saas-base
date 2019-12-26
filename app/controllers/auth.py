from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt

from app.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.account import Account
from app.controllers.account import get_account
from app.controllers.account import get_account_by_email
from app.models.account import Password


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(db: Session, username: str, plaintext_password: str):
    account_obj = get_account_by_email(db, email=username)
    if not account_obj:
        return False

    password_obj = (
        db.query(Password).filter_by(account_id=account_obj.id)
        .order_by(Password.created_on.desc())
        .first()
    )
    if not password_obj.is_correct_password(plaintext_password):
        return False
    return account_obj


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt