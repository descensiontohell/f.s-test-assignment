import datetime
from typing import List

from pydantic import BaseModel

from src.app.services.message.schemes import MessageFull


class MailingBase(BaseModel):
    mail_text: str
    user_filter: str
    start_time: datetime.datetime
    end_time: datetime.datetime


class Mailing(MailingBase):
    id: int


class MailingCreate(MailingBase):
    ...


class MailingUpdate(MailingBase):
    mail_text: str = None
    user_filter: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None


class MailingUpdatedResponse(BaseModel):
    id: int


class Stats(BaseModel):
    failed: int
    delivered: int


class MailingStats(Mailing):
    messages: Stats


class MailingMessages(Mailing):
    messages: List[MessageFull]


class MailingDeletedResponse(BaseModel):
    id: int
