from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import tenant as schemas
from app.models.tenant import Tenant, TenantAccount

from app.controllers.billing import stripe
from app.controllers.account import create_account


def get_tenant(db_session: Session, id: int):
    return db_session.query(Tenant).filter(Tenant.id == id).first()


def get_tenants(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(Tenant).offset(skip).limit(limit).all()


def add_account_to_tenant(db_session: Session, account_id, tenant_id):
    """Create relationship between tenant and account."""

    tenant_account_obj = TenantAccount(tenant_id=tenant_id, account_id=account_id)

    db_session.add(tenant_account_obj)
    db_session.commit()
    return tenant_account_obj


def create_tenant_and_account(
    db_session: Session,
    name: str,
    slug: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    is_active: bool = False,
    is_verified: bool = False,
    do_send_emails: bool = True
):
    """Create a tenant and an account."""

    tenant_obj = Tenant(name=name, slug=slug, billing_email=email)
    db_session.add(tenant_obj)
    db_session.flush()

    # New tenant = New Customer in stripe.
    customer_resp = stripe.Customer.create(
        email=email,
        description="Customer for {}<{}>".format(name, email),
        name=name,
        metadata={"tenant_id": tenant_obj.id},
    )

    # Record the Customer ID from stripe.
    tenant_obj.stripe_customer_id = customer_resp.get("id")

    db_session.commit()

    # Create account
    account_obj = create_account(
        db_session,
        first_name,
        last_name,
        email,
        password,
        is_active=is_active,
        is_verified=is_verified,
        send_registration_email=do_send_emails
    )

    # Add relationship between account to tenant.
    add_account_to_tenant(db_session, account_obj.id, tenant_obj.id)

    db_session.refresh(tenant_obj)

    return tenant_obj


def get_tenant_by_name(db_session: Session, name: str):
    """Get a tenant by name."""
    return db_session.query(Tenant).filter(Tenant.name == name).first()
