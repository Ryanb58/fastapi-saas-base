from typing import List

from pydantic import BaseModel

class AccountBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: int
    is_system_admin: bool

    class Config:
        orm_mode = True
