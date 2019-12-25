
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies.tenant import get_tenant
from app.schemas import account as schemas  
from app.dependencies.auth import get_current_account
from app.models.tenant import Tenant


router = APIRouter()

@router.get("/random")
def random(tenant_obj: Tenant = Depends(get_tenant), db: Session = Depends(get_db)):
    if not tenant_obj:
        tenant_obj = Tenant(
            name="Ten 1",
            slug="ten-1",
        )
        db.add(tenant_obj)
        db.commit()
    return tenant_obj
