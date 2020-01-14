from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_409_CONFLICT

from app.dependencies import get_db
from app.controllers.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
)
from app.dependencies.auth import get_current_account
from app.schemas.tenant import TenantAccountCreate
from app.controllers.tenant import create_tenant_and_account
from app.controllers.account import mark_account_as_verified_and_active

router = APIRouter()


@router.post("/verify", status_code=HTTP_200_OK)
def verify_account(token: str = "", db_session: Session = Depends(get_db)):
    mark_account_as_verified_and_active(db_session, token)
    return


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    account_obj = authenticate_user(db_session, form_data.username, form_data.password)
    if not account_obj:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Account must be active.
    if not account_obj.is_active:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Account disabled",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account_obj.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=HTTP_201_CREATED)
def register(
    tenant_account: TenantAccountCreate, db_session: Session = Depends(get_db)
):
    tenant_obj = create_tenant_and_account(
        db_session,
        tenant_account.name,
        tenant_account.slug,
        tenant_account.first_name,
        tenant_account.last_name,
        tenant_account.email,
        tenant_account.password,
    )
    if not tenant_obj:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Error creating new account/tenant.",
        )
    return {"msg": "Please check your email."}
