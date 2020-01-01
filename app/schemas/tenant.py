from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str
    billing_email: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    slug: str

    class Config:
        orm_mode = True

class TenantAccountCreate(BaseModel):
    name: str
    slug: str
    first_name: str
    last_name: str
    email: str
    password: str
