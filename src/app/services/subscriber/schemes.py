
from pydantic import BaseModel


class SubscriberBase(BaseModel):
    phone: str
    provider_code: str
    tag: str
    time_zone: str


class SubscriberCreate(SubscriberBase):
    id: int = None


class SubscriberUpdate(SubscriberBase):
    phone: str = None
    provider_code: str = None
    tag: str = None
    time_zone: str = None


class Subscriber(SubscriberBase):
    id: int


class SubscriberDeletedResponse(BaseModel):
    id: int
