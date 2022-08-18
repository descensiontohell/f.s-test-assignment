from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.subscriber.models import SubscriberModel
from src.app.services.subscriber.schemes import SubscriberCreate, Subscriber
from src.core.base_crud import CRUDBase


class SubscriberService(CRUDBase):
    def __init__(self):
        super().__init__(model=SubscriberModel)

    async def create_subscriber(self, session: AsyncSession, obj_in: SubscriberCreate) -> Subscriber:
        subscriber_model = await self.save(session=session, obj_in=obj_in)
        return subscriber_model

    async def get_by_phone(self, session: AsyncSession, phone: str) -> SubscriberModel:
        stmt = select(self.model).where(self.model.phone == phone)
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        return db_obj


subscriber_service = SubscriberService()
