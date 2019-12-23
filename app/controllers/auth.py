from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt

from app.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.auth import TokenData
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


async def get_current_account(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id: str = payload.get("sub")
        if account_id is None:
            raise credentials_exception
        token_data = TokenData(account_id=account_id)
    except PyJWTError:
        raise credentials_exception
    account = get_account(db, id=token_data.account_id)
    if account is None:
        raise credentials_exception
    return account


# async def get_current_active_account(current_user: Account = Depends(get_current_account)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
