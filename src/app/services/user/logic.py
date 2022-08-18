import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.models import MailingModel
from src.app.services.mailing.schemes import Mailing, MailingCreate
from src.app.services.user.models import UserModel
from src.app.services.user.schemes import UserCreate, User
from src.core.base_crud import CRUDBase


class UserService(CRUDBase):
    def __init__(self):
        super().__init__(model=UserModel)

    async def create_user(self, session: AsyncSession, obj_in: UserCreate) -> User:
        user_model = await self.save(session=session, obj_in=obj_in)
        return user_model

    async def get_by_phone(self, session: AsyncSession, phone: str) -> UserModel:
        stmt = select(self.model).where(self.model.phone == phone)
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        return db_obj

user_service = UserService()
