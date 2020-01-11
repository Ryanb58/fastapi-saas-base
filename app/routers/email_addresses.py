from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.dependencies import get_db
from app.schemas import account as schemas
from app.controllers.account import (
    get_email_addresses,
    create_email_address,
    get_account_by_email,
    verify_email_address,
)
from app.dependencies.auth import get_current_account

router = APIRouter()


@router.post("/verify", status_code=HTTP_200_OK)
def verify_email(token: str = "", db_session: Session = Depends(get_db)):
    verify_email_address(db_session, token)
    return


@router.post("", response_model=schemas.EmailAddress, status_code=HTTP_201_CREATED)
def create_one(
    email: schemas.EmailAddressCreate,
    db_session: Session = Depends(get_db),
    current_user: schemas.Account = Depends(get_current_account),
):
    # Can not add an email address that is already in use.
    db_email = get_account_by_email(db_session, email=email.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Set the account_id from the current logged in user.
    account_id = current_user.id

    return create_email_address(db_session, email.email, account_id)


@router.get("", response_model=List[schemas.EmailAddress], status_code=HTTP_200_OK)
def read_many(
    skip: int = 0,
    limit: int = 100,
    db_session: Session = Depends(get_db),
    current_user: schemas.Account = Depends(get_current_account),
):
    return get_email_addresses(
        db_session, account_id=current_user.id, skip=skip, limit=limit
    )
