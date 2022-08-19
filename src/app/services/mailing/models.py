from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.app.services.mailing.schemes import Mailing, MailingStats, Stats, MailingMessages
from src.app.services.message.models import MessageStatus
from src.core.database import Base


class MailingModel(Base):
    __tablename__ = "mailings"
    id = Column(Integer, primary_key=True)
    mail_text = Column(String)
    user_filter = Column(String)
    start_time = Column(DateTime(timezone=False), nullable=False)
    end_time = Column(DateTime(timezone=False), nullable=False)
    messages = relationship("MessageModel")

    def to_pd(self):
        return Mailing(**self.__dict__)

    def to_stats(self):
        failed = [m for m in self.messages if m and m.status == MessageStatus.failed]
        delivered = [m for m in self.messages if m and m.status == MessageStatus.delivered]
        d = self.__dict__
        d.pop("messages")
        return MailingStats(
            messages=Stats(delivered=len(delivered), failed=len(failed)),
            **d,
        )

    def to_ext(self):
        d = self.__dict__
        d["messages"] = [m.to_pd() for m in self.messages if m]
        return MailingMessages(**d)
