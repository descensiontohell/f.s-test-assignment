import datetime

from pydantic import BaseModel

from src.app.services.message.schemes import Message


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


class MailingStats(Mailing):
    messages: Message
    delivered_messages: int
    failed_messages: int
