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
from app.settings import SECRET_KEY
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

# to get a string like this run:
# openssl rand -hex 32
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(db_session: Session, username: str, plaintext_password: str):
    account_obj = get_account_by_email(db_session, email=username)

    # Must have an account.
    if not account_obj:
        return False

    password_obj = (
        db_session.query(Password)
        .filter_by(account_id=account_obj.id)
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
