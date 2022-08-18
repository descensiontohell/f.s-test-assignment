from sqlalchemy.orm import relationship

from src.app.services.user.schemes import User
from src.core.database import Base

from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String(11), unique=True)
    provider_code = Column(String)
    tag = Column(String)
    time_zone = Column(String)
    messages = relationship("MessageModel")

    def to_pd(self):
        return User(**self.__dict__)
