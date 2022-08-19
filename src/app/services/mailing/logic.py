import asyncio
import datetime
from typing import List
from collections import deque

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.services.mailing.mailer import Mailer
from src.app.services.mailing.models import MailingModel
from src.app.services.mailing.schemes import MailingCreate, Mailing, MailingStats
from src.app.services.subscriber.logic import subscriber_service
from src.core.base_crud import CRUDBase


class MailingService(CRUDBase):
    def __init__(self):
        super().__init__(model=MailingModel)

    async def create_mailing(self, session: AsyncSession, obj_in: MailingCreate) -> MailingModel:
        """
        Adds new mailing to the database

        :param session: AsyncSession
        :param obj_in: MailingCreate
        :return: MailingModel
        """

        model = await self.save(session=session, obj_in=obj_in)
        return model

    def schedule_mailing(self, session: AsyncSession, mailing: Mailing) -> None:
        """
        Starts poll task based on given mailing attributes

        :param session: AsyncSession
        :param mailing: Mailing
        :return: None
        """

        self.logger.warning("CREATED TASK")
        asyncio.create_task(self.poll(db=session, mailing=mailing))

    async def poll(self, db: AsyncSession, mailing: Mailing) -> None:
        """
        An asyncio task that waits for the mailing start time and initializes the mailing if it's not canceled

        :param db: AsyncSession
        :param mailing: Mailing
        :return: None
        """

        while True:
            self.logger.warning(f"Polling for mailing id={mailing.id}")
            await asyncio.sleep(3)
            now = datetime.datetime.now()
            if now > mailing.end_time:
                return
            if now > mailing.start_time:
                self.logger.warning(f"Initializing mailing {mailing.id}")
                return await self.initialize_mailing_if_not_canceled(session=db, m=mailing)

    async def initialize_mailing_if_not_canceled(self, session: AsyncSession, m: Mailing) -> None:
        """
        Checks if mailing still exists, gets its subscribers and initializes the mailing

        :param session: AsyncSession
        :param m: Mailing
        :return:
        """

        model = await self.get(session=session, id=m.id)
        if not model:
            return
        mailing = model.to_pd()

        subscribers = await subscriber_service.get_mailing_subscribers(session=session, mailing=mailing)
        subs_queue = deque(subscribers)
        self.logger.warning(f"OBTAINED SUBSCRIBERS: {subs_queue}")

        Mailer(mailing=mailing, subs=subs_queue, db=session)

    async def get_mailing_stats(self, session: AsyncSession) -> List[MailingStats]:
        """
        Returns a list of mailings and message stats

        :param session: AsyncSession
        :return: List[MailingStats]
        """

        stmt = select(self.model).options(selectinload(self.model.messages))
        coro = await session.execute(stmt)
        db_obj_list = coro.scalars()
        return [o.to_stats() for o in db_obj_list if o]

    async def get_mailing(self, id: int, session: AsyncSession) -> MailingModel:
        """
        Returns MailingModel by id

        :param id: int
        :param session: AsyncSession
        :return: MailingModel
        """

        stmt = select(self.model).options(selectinload(self.model.messages)).where(self.model.id == id)
        coro = await session.execute(stmt)
        obj = coro.scalar()
        return obj

    async def is_running(self, id: int, session: AsyncSession) -> bool:
        """
        Checks if datetime.now() is between mailing start time and end time

        :param id: int
        :param session: AsyncSession
        :return: bool
        """

        model = await self.get(session=session, id=id)
        now = datetime.datetime.now()
        if model.start_time < now < model.end_time:
            return True
        else:
            return False


mailing_service = MailingService()
