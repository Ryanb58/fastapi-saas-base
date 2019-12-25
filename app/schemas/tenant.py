from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    slug: str

    class Config:
        orm_mode = True
