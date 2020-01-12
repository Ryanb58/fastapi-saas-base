from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str


class TenantCreate(TenantBase):
    billing_email: str


class Tenant(TenantBase):
    id: int
    slug: str

    class Config:
        orm_mode = True


class TenantDetails(Tenant):
    billing_email: str


class TenantAccountCreate(BaseModel):
    name: str
    slug: str
    first_name: str
    last_name: str
    email: str
    password: str
