from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime
# Shared properties
from app.models import UserModel
from app.models.user import ROLE


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None
    avatar: Optional[str] = None
    phone: str = None
    registrationDate: datetime = None
    role: ROLE = None

    job: str = None
    organization: str = None
    location: str = None
    introduction: str = None
    personalWebsite: str = None
    jobName: str = None
    organizationName: str = None
    locationName: str = None

    class Config:
        orm_mode = True


class InUser(BaseModel):
    username: str = None
    password: str = None


class OutUser(UserBase):
    pass


# def from_user_model(self, user: User):
#     self.username = user.username
#     self.email = EmailStr(user.email)
#     self.avatar = user.avatar
#     self.is_superuser = user.is_superuser
#     self.role = user.role
#     self.registrationDate = user.registrationDate
#     self.is_active = user.is_active
#
#     self.phone = user.phone
#     self.organizationName = user.organizationName
#     self.organization = user.organization
#     self.jobName = user.jobName
#     self.job = user.job
#     self.locationName = user.locationName
#     self.introduction = user.introduction
#     self.location = user.location
#     self.personalWebsite = user.personalWebsite

# return self


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
