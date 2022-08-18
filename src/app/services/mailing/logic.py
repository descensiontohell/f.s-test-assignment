from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.models import MailingModel
from src.app.services.mailing.schemes import Mailing, MailingCreate
from src.core.base_crud import CRUDBase


class MailingService(CRUDBase):
    def __init__(self):
        super().__init__(model=MailingModel)

    async def create_mailing(self, session: AsyncSession, obj_in: MailingCreate) -> MailingModel:
        model = await self.save(session=session, obj_in=obj_in)
        return model
