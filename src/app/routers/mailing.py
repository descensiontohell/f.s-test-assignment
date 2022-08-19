from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.mailing.logic import mailing_service
from src.app.services.mailing.schemes import Mailing, MailingCreate, MailingStats, MailingMessages, MailingUpdate, \
    MailingDeletedResponse, MailingUpdatedResponse
from src.core.database import get_db

router = APIRouter(
    prefix="/mailings",
    tags=["mailings"],
)


@router.post(
    path="/",
    response_model=Mailing,
    description="Creates new mailing with given attributes\n\nRequires datetime in naive format: 2022-08-19 14:35:58",
)
async def create_mailing(mailing: MailingCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a new mailing

    :param mailing: MailingCreate
    :param db: AsyncSession
    :return: Mailing
    """

    new_m = await mailing_service.create_mailing(session=db, obj_in=mailing)
    mailing_service.schedule_mailing(session=db, mailing=new_m.to_pd())
    return new_m.to_pd()


@router.get(
    path="/",
    response_model=List[MailingStats],
    description="Get all mailings and their message stats",
)
async def get_mailings(db: AsyncSession = Depends(get_db)):
    """
    Returns all mailings

    :param db: AsyncSession
    :return: List[MailingStats]
    """

    models = await mailing_service.get_mailing_stats(session=db)
    return models


@router.get(
    path="/{mailing_id}",
    response_model=MailingMessages,
    description="Get mailing attributes with message list",
    responses={404: {"description": "Mailing not found"}}
)
async def get_single_mailing(mailing_id: int, db: AsyncSession = Depends(get_db)):
    """
    Returns mailing with messages if exists, 404 if not

    :param mailing_id: int
    :param db: AsyncSession
    :return: MailingMessages
    """

    model = await mailing_service.get_mailing(id=mailing_id, session=db)
    if not model:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return model.to_ext()


@router.put(
    path="/{mailing_id}",
    response_model=MailingUpdatedResponse,
    description="Update mailing if it's not running\n\nRequires datetime in naive format: 2022-08-19 14:35:58",
    responses={
        400: {"description": "Can't update running mailing"},
        404: {"description": "Mailing not found"},
    },
)
async def update_mailing(mailing_id: int, updated_obj: MailingUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates mailing

    Cannot update between start time and end time (returns 400 on attempt)

    404 if not found

    :param mailing_id: int
    :param updated_obj: MailingUpdate
    :param db: AsyncSession
    :return: MailingUpdatedResponse
    """

    target_model = await mailing_service.get(session=db, id=mailing_id)
    if not target_model:
        raise HTTPException(status_code=404, detail="Mailing with given id not found")

    if await mailing_service.is_running(id=mailing_id, session=db):
        raise HTTPException(status_code=400, detail="Can't update running mailing")

    await mailing_service.update(session=db, db_obj=target_model, obj_in=updated_obj)
    return MailingUpdatedResponse(id=mailing_id)


@router.delete(
    path="/{mailing_id}",
    response_model=MailingDeletedResponse,
    description="Delete mailing by id if it's not running",
    responses={
     400: {"description": "Can't delete running mailing"},
     404: {"description": "Mailing not found"},
    },
)
async def delete_mailing(mailing_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes mailing if exists, 404 if not

    :param mailing_id: int
    :param db: AsyncSession
    :return: MailingDeletedResponse
    """

    target_model = await mailing_service.get(session=db, id=mailing_id)
    if not target_model:
        raise HTTPException(status_code=404, detail="Mailing with given id not found")

    if await mailing_service.is_running(id=mailing_id, session=db):
        raise HTTPException(status_code=400, detail="Can't delete running mailing")

    await mailing_service.delete(session=db, id=mailing_id)
    return MailingDeletedResponse(id=mailing_id)
