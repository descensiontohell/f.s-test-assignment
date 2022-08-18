import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func

from src.core.database import Base


class MessageStatus(enum.Enum):
    delivered = "delivered"
    failed = "failed"


class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sent_at = Column(DateTime, server_default=func.now())
    status = Column(Enum(MessageStatus))
    mailing_id = Column(Integer, ForeignKey("mailings.id"))
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
