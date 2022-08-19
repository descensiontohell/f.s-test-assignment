import datetime

from pydantic import BaseModel

from src.app.services.message.models import MessageStatus


class Message(BaseModel):
    id: int = None
    sent_at: datetime.datetime = None
    status: MessageStatus


class MessageCreate(Message):
    mailing_id: int
    subscriber_id: int


class MessageFull(MessageCreate):
    ...
