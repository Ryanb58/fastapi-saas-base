"""
Control the members that are apart of a Tenant.
"""
from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import tenant as schemas
from app.models.tenant import Tenant, TenantAccount
from app.models.account import EmailAddress
from app.controllers.billing import stripe
from app.controllers.account import create_account
from app.controllers.account import get_account_by_email
from app.utils.email import send_email
from app.settings import FRONTEND_BASE_URL
from app.settings import LOGIN_URL_PATH


def get_members(db_session: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return (
        db_session.query(TenantAccount)
        .filter(TenantAccount.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_member_by_email(db_session: Session, tenant_id: int, email: str):
    """Return the member if they are apart of this tenant."""
    account_obj = get_account_by_email(db_session, email)
    # Check if email address exists.
    return (
        db_session.query(TenantAccount)
        .filter(
            TenantAccount.tenant_id == tenant_id, TenantAccount.account == account_obj
        )
        .first()
    )


def add_member(
    db_session: Session, tenant_id: int, email: str, do_send_email: bool = True
):
    """Add a new member to the tenant."""
    tenant_obj = db_session.query(Tenant).get(tenant_id)
    # If email address:
    email_obj = (
        db_session.query(EmailAddress).filter(EmailAddress.email == email).first()
    )
    if email_obj and email_obj.account:
        # Account already exists, go ahead and add them.
        tenant_account_obj = TenantAccount()
        tenant_account_obj.tenant_id = tenant_id
        tenant_account_obj.account_id = email_obj.account_id
        db_session.add(tenant_account_obj)
        db_session.commit()

        # TODO: Send email telling them we added them.
        if do_send_email:
            # send_email()
            # Send the email!
            send_email(
                to_email=email,
                subject=f"You've been added to {tenant_obj.name}",
                body=(
                    f"Weclome to {tenant_obj.name}."
                    f"<p />You have been invited into the new group. Please use the link below to login."
                    f"<p /><a href='{FRONTEND_BASE_URL}{LOGIN_URL_PATH}'>Login</a>"
                ),
            )
    else:
        # Never been apart of this site.
        # Create relationship
        tenant_account_obj = TenantAccount()
        tenant_account_obj.tenant_id = tenant_id
        tenant_account_obj.email_address = email
        db_session.add(tenant_account_obj)
        db_session.commit()
        # Send registration invite.
