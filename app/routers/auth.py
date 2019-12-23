from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.dependencies import get_db
from app.controllers.auth import get_current_account, ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token
from app.schemas.account import Account
router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    account = authenticate_user(db, form_data.username, form_data.password)
    if not account:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=Account)
async def read_users_me(current_user: Account = Depends(get_current_account)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: Account = Depends(get_current_account)):
    return [{"item_id": "Foo", "owner": current_user.username}]
