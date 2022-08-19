from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.logic import mailing_service
from src.app.services.mailing.schemes import Mailing, MailingCreate
from src.core.database import get_db

router = APIRouter(
    prefix="/mailings",
    tags=["mailings"],
)


@router.post(
    path="/",
    response_model=Mailing,
    description="Creates new mailing with given attributes",
)
async def create_mailing(mailing: MailingCreate, db: AsyncSession = Depends(get_db)):
    new_m = await mailing_service.create_mailing(session=db, obj_in=mailing)
    mailing_service.schedule_mailing(session=db, mailing=new_m.to_pd())
    return new_m.to_pd()
