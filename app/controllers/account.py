from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import Depends
import jwt

from app.config import config
from app.schemas import account as schemas
from app.models.account import Account
from app.models.account import EmailAddress
from app.models.account import Password
from app.utils.email import send_email

#### Accounts

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = config("SECRET_KEY", cast=str, default=False)
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 30
FRONTEND_URL = config("FRONTEND_URL", cast=str)


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
    send_registration_email: bool = True,
):
    """Create an user account."""
    account_obj = Account(
        first_name=first_name,
        last_name=last_name,
        is_system_admin=is_system_admin,
        is_active=is_active,
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

    # Send registration email.
    if send_registration_email:
        token = create_email_verification_token(email_obj)
        registration_link = "{}/{}/verify?token={}".format(
            FRONTEND_URL,
            email_obj.id, 
            token
        )
        send_email(
            to_email=email,
            subject="Welcome!",
            body="""Weclome to the website. 
            <p />Please use the following link to continue your registration. 
            <p /><a href="{}">{}</a>
            """.format(
                registration_link,
                registration_link
            ),
        )

    db_session.refresh(account_obj)

    return account_obj


#### Email Addresses


def get_email_addresses(
    db_session: Session, account_id: int = None, skip: int = 0, limit: int = 100
):
    return (
        db_session.query(EmailAddress)
        .filter(EmailAddress.account_id == account_id)
        .all()
        or []
    )


def create_email_address(db_session: Session, email: str, account_id: int):
    """Add an email_address to a users account."""
    email_obj = EmailAddress(
        account_id=account_id, email=email, primary=False, verified=False
    )

    db_session.add(email_obj)
    db_session.commit()
    db_session.refresh(email_obj)

    return email_obj


def create_email_verification_token(email_obj):
    """
    Create a token that can be used to verify a email address.
    
    Expires in 1 hour.
    """
    to_encode = {
        "id": email_obj.id,
    }
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode("utf-8")

def get_email_id_from_token(token):
    """Mark an email as verified if token is legit."""
    try:
        token = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
    except jwt.ExpiredSignatureError:
        # Signature has expired
        return False
    except Exception:
        return False

    return token.get('id')

def mark_email_as_verified(db_session: Session, email_id: int):
    """Mark an email id as verified and account as active."""
    email_obj = db_session.query(EmailAddress).get(email_id)
    
    # Mark email as verified.
    email_obj.verified = True
    email_obj.verified_on = datetime.now()
    # Mark account as active.
    account_obj = email_obj.account
    account_obj.is_active = True

    db_session.add(account_obj)
    db_session.add(email_obj)
    db_session.commit()

def verify_email_address(db_session: Session, token: str):
    email_id = get_email_id_from_token(token)
    if not email_id:
        raise NotImplementedError("Token not valid or email_id wrong...")

    mark_email_as_verified(db_session, email_id)
