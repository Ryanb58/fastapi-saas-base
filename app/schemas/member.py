from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenantAccount(BaseModel):
    id: int
    account_id: int
    tenant_id: int

    class Config:
        orm_mode = True


class MemberCreate(BaseModel):
    tenant_id: int
    email: str
