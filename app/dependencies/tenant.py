from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.tenant import Tenant


async def get_tenant(tenant_id: int = None, db: Session = Depends(get_db)):
    """Get the tenant id from the url."""
    if not tenant_id:
        return None
    return db.query(Tenant).get(tenant_id)

