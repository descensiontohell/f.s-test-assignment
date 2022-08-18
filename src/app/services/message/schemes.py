import datetime

from pydantic import BaseModel

from src.app.services.message.models import MessageStatus


class Message(BaseModel):
    id: int
    sent_at: datetime.datetime
    status: MessageStatus
