from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import account as schemas  
from app.controllers.account import get_account_email_addresses
from app.dependencies.auth import get_current_account

router = APIRouter()

# @router.post("/", response_model=schemas.Account)
# def create_one(account: schemas.AccountCreate, db: Session = Depends(get_db), current_user: schemas.Account = Depends(get_current_account)):
#     db_account = get_account_by_email(db, email=account.email)
#     if db_account:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Can not create a system admin if you yourself are not one.
#     if not current_user.is_system_admin:
#         account.is_system_admin = False

#     return create_account(db, account=account)


@router.get("/", response_model=List[schemas.EmailAddress])
def read_many(account_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    email_objs = get_account_email_addresses(db, account_id, skip=skip, limit=limit)
    return email_objs

# @router.get("/me", response_model=schemas.Account)
# async def read_me(current_user: schemas.Account = Depends(get_current_account)):
#     """Get logged in user details."""
#     return current_user


# @router.get("/{id}", response_model=schemas.Account)
# def read_one(id: int, db: Session = Depends(get_db)):
#     db_account = get_account(db, id=id)
#     if db_account is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_account
