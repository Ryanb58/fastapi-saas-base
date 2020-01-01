from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import account as schemas
from app.models.account import Account
from app.models.account import EmailAddress
from app.models.account import Password

# Accounts


def get_account(db_session: Session, id: int):
    return db_session.query(Account).filter(Account.id == id).first()


def get_account_by_email(db_session: Session, email: str):
    email_obj = (
        db_session.query(EmailAddress).filter(EmailAddress.email == email).first()
    )
    if not email_obj:
        return None
    return email_obj.account


def get_accounts(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(Account).offset(skip).limit(limit).all()


def create_account(
    db_session: Session,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    is_system_admin: bool = False,
    is_active: bool = False,
):
    """Create an user account."""
    account_obj = Account(
        first_name=first_name, last_name=last_name, is_system_admin=is_system_admin, is_active=is_active
    )
    db_session.add(account_obj)
    db_session.flush()

    email_obj = EmailAddress(
        account_id=account_obj.id, email=email, primary=True, verified=False
    )

    password_obj = Password(account_id=account_obj.id, password=password)

    db_session.add(email_obj)
    db_session.add(password_obj)
    db_session.commit()
    db_session.refresh(account_obj)

    return account_obj


# Email Addresses


def get_email_addresses(
    db_session: Session, account_id: int = None, skip: int = 0, limit: int = 100
):
    return (
        db_session.query(EmailAddress)
        .filter(EmailAddress.account_id == account_id)
        .all()
        or []
    )


def create_email_address(db_session: Session, email: schemas.EmailAddressCreate):
    """Add an email_address to a users account."""
    email_obj = EmailAddress(
        account_id=email.account_id, email=email.email, primary=False, verified=False
    )

    db_session.add(email_obj)
    db_session.commit()
    db_session.refresh(email_obj)

    return email_obj
