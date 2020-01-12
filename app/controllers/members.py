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
    return db_session.query(TenantAccount).filter(
            TenantAccount.tenant_id == tenant_id,
            TenantAccount.account == account_obj
        ).first()


def add_member(db_session: Session, tenant_id: int, email: str):
    """Add a new member to the tenant."""

    # If email address:
    email_obj = (
        db_session.query(EmailAddress).filter(EmailAddress.email == email).first()
    )
    if email_obj:
        # Must of already been invited, or has existing account.
        if email_obj.account:
            # Account already exists, go ahead and add them.
            tenant_account_obj = TenantAccount()
            tenant_account_obj.tenant_id = tenant_id
            tenant_account_obj.account_id = email_obj.account_id
            db_session.add(tenant_account_obj)
            db_session.commit()
            
            # Send email telling them we added them.
        else:
            # Account DNE:
            tenant_account_obj = TenantAccount()
            tenant_account_obj.tenant_id = tenant_id
            tenant_account_obj.email_address_id = email_obj.id
            db_session.add(tenant_account_obj)
            db_session.commit()

            # Send email telling them we added them and would like them to register.
    else:
        # Never been apart of this site.
        
        # Create email obj without an account object.

        # Create relationship
        tenant_account_obj = TenantAccount()
        tenant_account_obj.tenant_id = tenant_id
        tenant_account_obj.email_address_id = email_obj.id
        db_session.add(tenant_account_obj)
        db_session.commit()
        # Send registration invite.

