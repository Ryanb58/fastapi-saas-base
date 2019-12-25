from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import tenant as schemas  
from app.models.tenant import Tenant


def get_tenant(db: Session, id: int):
    return db.query(Tenant).filter(Tenant.id == id).first()

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tenant).offset(skip).limit(limit).all()

def create_tenant(db: Session, tenant: schemas.TenantCreate):
    """Create a tenant."""
    tenant_obj = Tenant(
        name=tenant.name,
        slug=tenant.slug,
    )
    db.add(tenant_obj)
    db.commit()
    db.refresh(tenant_obj)

    return tenant_obj

def get_tenant_by_name(db: Session, name: str):
    """Get a tenant by name."""
    return db.query(Tenant).filter(Tenant.name == name).first()
