from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str
    slug: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int

    class Config:
        orm_mode = True
