from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
import app.schemas as schemas
from app.controllers.tenant import get_tenant_by_name
from app.controllers.tenant import get_tenant
from app.controllers.tenant import get_tenants

# from app.controllers.tenant import create_tenant
from app.dependencies.auth import get_current_account

router = APIRouter()

# @router.post("/", response_model=schemas.Tenant)
# def create_one(tenant: schemas.TenantCreate, db_session: Session = Depends(get_db), current_user: schemas.Account = Depends(get_current_account)):
#     db_tenant = get_tenant_by_name(db_session, name=tenant.name)
#     if db_tenant:
#         raise HTTPException(status_code=400, detail="Name already registered")

#     return create_tenant(db_session, tenant=tenant)


@router.get("/", response_model=List[schemas.Tenant])
def read_many(skip: int = 0, limit: int = 100, db_session: Session = Depends(get_db)):
    tenants = get_tenants(db_session, skip=skip, limit=limit)
    return tenants


@router.get("/{id}", response_model=schemas.TenantDetails)
def read_one(id: int, db_session: Session = Depends(get_db)):
    db_tenant = get_tenant(db_session, id=id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant
