
from pydantic import BaseModel


class SubscriberBase(BaseModel):
    phone: int
    provider_code: str
    tag: str
    time_zone: str


class SubscriberCreate(SubscriberBase):
    id: int = None


class SubscriberUpdate(SubscriberBase):
    phone: int = None
    provider_code: str = None
    tag: str = None
    time_zone: str = None


class Subscriber(SubscriberBase):
    id: int


class SubscriberDeletedResponse(BaseModel):
    id: int
