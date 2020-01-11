from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.dependencies import get_db
from app.schemas import tenant as schemas
from app.controllers.members import get_members
from app.dependencies.auth import get_current_account

router = APIRouter()


@router.get("", response_model=List[schemas.TenantAccount], status_code=HTTP_200_OK)
def read_many(
    skip: int = 0,
    limit: int = 100,
    tenant_id: int = None,
    db_session: Session = Depends(get_db),
):
    return get_members(db_session, tenant_id=tenant_id, skip=skip, limit=limit)
