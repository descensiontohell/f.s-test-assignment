
from pydantic import BaseModel


class UserBase(BaseModel):
    phone: str
    provider_code: str
    tag: str
    time_zone: str


class UserCreate(UserBase):
    id: int = None


class UserUpdate(UserBase):
    phone: str = None
    provider_code: str = None
    tag: str = None
    time_zone: str = None


class User(UserBase):
    id: int


class UserDeletedResponse(BaseModel):
    id: int
