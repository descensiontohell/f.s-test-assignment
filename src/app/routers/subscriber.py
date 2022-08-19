from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.subscriber.logic import subscriber_service
from src.app.services.subscriber.schemes import Subscriber, SubscriberCreate, SubscriberDeletedResponse, \
    SubscriberUpdate
from src.core.database import get_db

router = APIRouter(
    prefix="/subscribers",
    tags=["subscribers"],
)


@router.get(
    path="/",
    response_model=List[Subscriber],
    description="Get all subscribers",
)
async def get_subscribers(db: AsyncSession = Depends(get_db)):
    """
    Returns all subscribers

    :param db: AsyncSession
    :return: List[Subscriber]
    """

    models = await subscriber_service.get_many(session=db)
    return [m.to_pd() for m in models if m]


@router.post(
    path="/",
    response_model=Subscriber,
    description="Creates new subscriber",
    responses={409: {"description": "Subscriber exists"}},
)
async def create_subscriber(subscriber: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates new subscriber

    :param subscriber: SubscriberCreate
    :param db: AsyncSession
    :return: Subscriber
    """
    model = await subscriber_service.get_by_phone(db, subscriber.phone)
    if model:
        raise HTTPException(status_code=409, detail="Subscriber with given phone exists")

    await subscriber_service.create_subscriber(db, subscriber)
    return (await subscriber_service.get_by_phone(db, subscriber.phone)).to_pd()


@router.put(
    path="/{user_id}",
    response_model=Subscriber,
    description="Updates existing subscriber",
    responses={404: {"description": "Subscriber not found"}},
)
async def update_subscriber(subscriber_id: int, user: SubscriberUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates subscriber by id if exists, 404 if not

    :param subscriber_id: int
    :param user: SubscriberUpdate
    :param db: AsyncSession
    :return: Subscriber
    """

    model = await subscriber_service.get(session=db, id=subscriber_id)
    if not model:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    await subscriber_service.update(session=db, db_obj=model, obj_in=user)
    return (await subscriber_service.get(session=db, id=subscriber_id)).to_pd()


@router.delete(
    path="/{user_id}",
    response_model=SubscriberDeletedResponse,
    description="Deletes existing subscriber",
    responses={404: {"description": "Subscriber not found"}},
)
async def delete_user(subscriber_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes user if exists, 404 if not

    :param subscriber_id: int
    :param db: AsyncSession
    :return: SubscriberDeletedResponse
    """

    model = await subscriber_service.get(session=db, id=subscriber_id)
    if not model:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    await subscriber_service.delete(session=db, id=subscriber_id)
    return SubscriberDeletedResponse(id=subscriber_id)
