import asyncio
import datetime
import logging
from collections import deque
from typing import List

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.schemes import Mailing
from src.app.services.message.logic import message_service
from src.app.services.message.models import MessageStatus
from src.app.services.message.schemes import MessageCreate
from src.app.services.subscriber.schemes import Subscriber
from src.core.config import settings


class Mailer:
    def __init__(self, mailing: Mailing, subs: deque[Subscriber], db: AsyncSession):
        self.mailing = mailing
        self.subs_q = subs
        self.logger = logging.getLogger(f"Mailer {mailing.id}")
        self.db = db
        self.headers = {"Authorization": f"Bearer {settings.AUTH_TOKEN}"}
        asyncio.create_task(self.mail())

    async def mail(self):
        while datetime.datetime.now() < self.mailing.end_time and self.subs_q:
            try:
                subscriber = self.subs_q.pop()
            except IndexError:
                continue
            message_id = await self.get_message_id(subscriber=subscriber)
            await self.send_message(subscriber=subscriber, message_id=message_id)
            await asyncio.sleep(0.5)

    async def send_message(self, subscriber: Subscriber, message_id: int):
        data = {
            "id": message_id,
            "phone": subscriber.phone,
            "text": self.mailing.mail_text,
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            url = f"{settings.URL_BASE}/{message_id}"
            resp = await session.post(
                url=url,
                json=data,
            )
            self.logger.error(f"{url}   {resp.status}   {data}")

            if resp.status != 200:
                self.subs_q.appendleft(subscriber)
                status = MessageStatus.failed
            else:
                status = MessageStatus.delivered

        self.logger.error(message_id)
        new_message = MessageCreate(
            id=message_id,
            sent_at=datetime.datetime.now(),
            status=status,
            subscriber_id=subscriber.id,
            mailing_id=self.mailing.id,
        )
        self.logger.error(new_message)
        await message_service.update_message(message_id=message_id, obj=new_message, db=self.db)

    async def get_message_id(self, subscriber: Subscriber) -> int:
        """
        Gets id of existing pending message or creates one and returns id

        :param subscriber: Subscriber
        :return: int
        """
        message = await message_service.get_by_subscriber_mailing(
            subscriber_id=subscriber.id,
            mailing_id=self.mailing.id,
            db=self.db,
        )
        self.logger.error(f"MESSAGE: {message}")
        if not message:
            self.logger.error(f"CREATING MESSAGE")
            message = await message_service.add_pending_message(
                MessageCreate(
                    status=MessageStatus.pending,
                    mailing_id=self.mailing.id,
                    subscriber_id=subscriber.id,
                ),
                db=self.db,
            )
        return message.id
