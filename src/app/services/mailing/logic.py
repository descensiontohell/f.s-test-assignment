import asyncio
import datetime
from select import select
from typing import List
from collections import deque

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.mailer import Mailer
from src.app.services.mailing.models import MailingModel
from src.app.services.mailing.schemes import MailingCreate, Mailing
from src.app.services.subscriber.logic import subscriber_service
from src.app.services.subscriber.schemes import Subscriber
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

        self.logger.info("CREATED TASK")
        asyncio.create_task(self.poll(db=session, mailing=mailing))

    async def poll(self, db: AsyncSession, mailing: Mailing) -> None:
        """
        An asyncio task that waits for the mailing start time and initializes the mailing if it's not canceled

        :param db: AsyncSession
        :param mailing: Mailing
        :return: None
        """

        while True:
            self.logger.error(f"Polling for mailing id={mailing.id}")
            await asyncio.sleep(3)
            now = datetime.datetime.now()
            if now > mailing.end_time:
                return
            if now > mailing.start_time:
                self.logger.error(f"Initializing mailing {mailing.id}")
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
        self.logger.error(f"OBTAINED SUBSCRIBERS: {subs_queue}")

        Mailer(mailing=mailing, subs=subs_queue, db=session)


mailing_service = MailingService()
