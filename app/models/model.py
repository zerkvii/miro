# for recursive
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False


# out Model is used in store and output, in Model is the api post data structure
class InUser(User):
    """
    for api use only
    """
    pass


class OutUser(User):
    """
    store in db
    """
    avatar: str = Field(...)
    email: str = Field(...)
    job: str = Field(...)
    jobName: str = Field(...)
    location: str = Field(...)
    locationName: str = Field(...)
    organization: str = Field(...)
    organizationName: str = Field(...)
    personalWebsite: str = Field(...)
    phone: str = Field(...)
    registrationDate: datetime = Field(...)
    role: str = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str


class TokenPayload(BaseModel):
    username: str = ""


class MetaInfo(BaseModel):
    locale: str = None
    requiresAuth: bool = None
    icon: str = None
    order: int = None


class MenuItem(BaseModel):
    children: List[MenuItem] = Field(...)
    path: str = Field(...)
    name: str = Field(...)
    meta: MetaInfo = Field(...)


class UserMenu(BaseModel):
    username: str = Field(...)
    menuList: List[MenuItem] = Field(...)
