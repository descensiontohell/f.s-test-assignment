import enum

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func

from src.core.database import Base


class MessageStatus(enum.Enum):
    delivered = "delivered"
    failed = "failed"
    pending = "pending"


class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sent_at = Column(DateTime, server_default=func.now())
    status = Column(Enum(MessageStatus))
    mailing_id = Column(Integer, ForeignKey("mailings.id"))
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))

    def to_pd(self):
        from src.app.services.message.schemes import MessageFull
        return MessageFull(**self.__dict__)
