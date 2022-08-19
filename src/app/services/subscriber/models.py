from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.app.services.subscriber.schemes import Subscriber
from src.core.database import Base
from src.app.services.message.models import MessageModel


class SubscriberModel(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True)
    phone = Column(Integer, unique=True)
    provider_code = Column(String)
    tag = Column(String)
    time_zone = Column(String)
    messages = relationship("MessageModel")

    def to_pd(self):
        return Subscriber(**self.__dict__)
