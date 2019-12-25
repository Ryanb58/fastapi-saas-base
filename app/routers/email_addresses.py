from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import account as schemas  
from app.controllers.account import get_email_addresses, create_email_address, get_account_by_email
from app.dependencies.auth import get_current_account

router = APIRouter()

@router.post("/", response_model=schemas.EmailAddress)
def create_one(
    email: schemas.EmailAddressCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.Account = Depends(get_current_account)
    ):

    # Can not add an email address that is already in use.
    db_email = get_account_by_email(db, email=email.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Set the account_id from the current logged in user.
    email.account_id = current_user.id

    return create_email_address(db, email)


@router.get("/", response_model=List[schemas.EmailAddress])
def read_many(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: schemas.Account = Depends(get_current_account)
    ):
    return get_email_addresses(db, account_id=current_user.id, skip=skip, limit=limit)
