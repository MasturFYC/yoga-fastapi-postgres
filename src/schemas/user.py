""" User Schema """

from typing import Optional
from pydantic import BaseModel

class UserIn(BaseModel):
    """ router parameter in """
    name: str
    email: str
    password: str
    role: str


class UserOut(UserIn):
    """ router parameter out """
    id: int

class UserLogin(BaseModel):
    """ user login parameter in """
    email: str
    password: str

class UserGet(BaseModel):
    """ user auth parameter out """
    id: int
    name: str
    email: str
    role: str
    token: Optional[str] = None
