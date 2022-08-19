from typing import List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.schemes import Mailing
from src.app.services.subscriber.models import SubscriberModel
from src.app.services.subscriber.schemes import SubscriberCreate, Subscriber
from src.core.base_crud import CRUDBase


class SubscriberService(CRUDBase):
    def __init__(self):
        super().__init__(model=SubscriberModel)

    async def create_subscriber(self, session: AsyncSession, obj_in: SubscriberCreate) -> Subscriber:
        """
        Adds new subscriber to the database

        :param session: AsyncSession
        :param obj_in: SubscriberCreate
        :return: Subscriber
        """

        subscriber_model = await self.save(session=session, obj_in=obj_in)
        return subscriber_model

    async def get_by_phone(self, session: AsyncSession, phone: int) -> SubscriberModel:
        """
        Returns subscriber by phone

        :param session: AsyncSession
        :param phone: int
        :return: SubscriberModel
        """

        stmt = select(self.model).where(self.model.phone == phone)
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        return db_obj

    async def get_mailing_subscribers(self, session: AsyncSession, mailing: Mailing) -> List[Subscriber]:
        """
        Returns subscribers that belong to given mailing

        :param session: AsyncSession
        :param mailing:
        :return: List[Subscriber]
        """

        f = mailing.user_filter
        stmt = select(self.model).filter(or_(self.model.tag.ilike(f"%{f}%"), self.model.provider_code.ilike(f"%{f}%")))
        coro = await session.execute(stmt)
        db_obj = coro.scalars().all()
        return [o.to_pd() for o in db_obj if o]


subscriber_service = SubscriberService()
