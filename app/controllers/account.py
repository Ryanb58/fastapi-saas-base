from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import account as schemas  
from app.models.account import Account
from app.models.account import EmailAddress
from app.models.account import Password


def get_account(db: Session, id: int):
    return db.query(Account).filter(Account.id == id).first()

def get_account_by_email(db: Session, email: str):
    email_obj = db.query(EmailAddress).filter(EmailAddress.email == email).first()
    if not email_obj:
        return None
    return email_obj.account

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    """Create an user account."""
    account_obj = Account(
        first_name=account.first_name,
        last_name=account.last_name,
        is_system_admin=account.is_system_admin
    )
    db.add(account_obj)
    db.flush()

    email_obj = EmailAddress(
        account_id=account_obj.id,
        email=account.email,
        primary=True,
        verified=False
    )

    password_obj = Password(
        account_id=account_obj.id,
        password=account.password
    )

    db.add(email_obj)
    db.add(password_obj)
    db.commit()
    db.refresh(account_obj)

    return account_obj

def get_account_email_addresses(db: Session, account_id: int, skip: int = 0, limit: int = 100):
    return db.query(EmailAddress).filter(EmailAddress.account_id == account_id).all() or []