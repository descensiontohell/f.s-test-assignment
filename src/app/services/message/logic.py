from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.message.models import MessageModel
from src.app.services.message.schemes import Message, MessageCreate
from src.core.base_crud import CRUDBase


class MessageService(CRUDBase):
    def __init__(self):
        super().__init__(model=MessageModel)

    async def update_message(self, message_id: int, obj: Message, db: AsyncSession) -> None:
        """
        Updates existing message by its id

        :param message_id: int
        :param obj: Message
        :param db: AsyncSession
        :return: None
        """

        data = obj.__dict__
        valid_data = {k: data[k] for k in data if data[k]}
        query = update(MessageModel).where(MessageModel.id == message_id).values(**valid_data)
        await db.execute(query)
        await db.commit()

    async def add_pending_message(self, message: MessageCreate, db: AsyncSession) -> MessageModel:
        """
        Adds pending message for given subscriber and mailing

        :param message: MessageCreate
        :param db: AsyncSession
        :return: MessageModel
        """

        obj_in_data = message.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_subscriber_mailing(self, subscriber_id: int, mailing_id: int, db: AsyncSession) -> MessageModel:
        """
        Returns message from database by subscriber.id and mailing.id

        :param subscriber_id: int
        :param mailing_id: int
        :param db: AsyncSession
        :return: MessageModel
        """

        stmt = select(self.model).where(self.model.subscriber_id == subscriber_id, self.model.mailing_id == mailing_id)
        coro = await db.execute(stmt)
        db_obj = coro.scalar()
        return db_obj


message_service = MessageService()
