from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.dependencies import get_db
from app.schemas import member as schemas
from app.schemas.account import Account as AccountSchema
from app.controllers.members import get_members
from app.controllers.members import get_member_by_email
from app.controllers.members import add_member
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


@router.post("", response_model=schemas.MemberCreate, status_code=HTTP_201_CREATED)
def add_one(
    member: schemas.MemberCreate,
    db_session: Session = Depends(get_db),
    current_user: AccountSchema = Depends(get_current_account),
):
    # Make sure email isn't already added.
    db_member = get_member_by_email(
        db_session, tenant_id=member.tenant_id, email=member.email
    )
    if db_member:
        raise HTTPException(status_code=400, detail="Account has already been invited.")

    # Invite the user.
    return add_member(db_session, tenant_id=member.tenant_id, email=member.email)
