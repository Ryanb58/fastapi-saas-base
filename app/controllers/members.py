"""
Control the members that are apart of a Tenant.
"""
from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import tenant as schemas
from app.models.tenant import Tenant, TenantAccount

from app.controllers.billing import stripe
from app.controllers.account import create_account


def get_members(db_session: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return db_session.query(TenantAccount).filter(
        TenantAccount.tenant_id == tenant_id
    ).offset(skip).limit(limit).all()
