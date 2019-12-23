from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import account as schemas  
from app.controllers.account import get_account_by_email
from app.controllers.account import get_account
from app.controllers.account import get_accounts
from app.controllers.account import create_account

router = APIRouter()

@router.post("/", response_model=schemas.Account)
def create_one(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_account(db=db, account=account)


@router.get("/", response_model=List[schemas.Account])
def read_many(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = get_accounts(db, skip=skip, limit=limit)
    return accounts


@router.get("/{id}", response_model=schemas.Account)
def read_one(id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, id=id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account
