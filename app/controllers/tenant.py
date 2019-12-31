from sqlalchemy.orm import Session
from fastapi import Depends
from slugify import slugify

from app.schemas import tenant as schemas  
from app.models.tenant import Tenant


def get_tenant(db_session: Session, id: int):
    return db_session.query(Tenant).filter(Tenant.id == id).first()

def get_tenants(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(Tenant).offset(skip).limit(limit).all()

def create_tenant(db_session: Session, tenant: schemas.TenantCreate):
    """Create a tenant."""
    tenant_obj = Tenant(
        name=tenant.name,
        slug=slugify(value) # Slug is only set once, must contact support to change.
    )
    db_session.add(tenant_obj)
    db_session.commit()
    db_session.refresh(tenant_obj)

    return tenant_obj

def get_tenant_by_name(db_session: Session, name: str):
    """Get a tenant by name."""
    return db_session.query(Tenant).filter(Tenant.name == name).first()
