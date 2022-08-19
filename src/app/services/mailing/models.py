from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.app.services.mailing.schemes import Mailing
from src.core.database import Base


class MailingModel(Base):
    __tablename__ = "mailings"
    id = Column(Integer, primary_key=True)
    mail_text = Column(String)
    user_filter = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    messages = relationship("MessageModel")

    def to_pd(self):
        return Mailing(**self.__dict__)
