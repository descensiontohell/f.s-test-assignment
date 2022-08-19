from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.app.services.subscriber.logic import subscriber_service
from src.app.services.subscriber.schemes import Subscriber, SubscriberCreate, SubscriberDeletedResponse, SubscriberUpdate
from src.core.database import get_db

router = APIRouter(
    prefix="/subscribers",
    tags=["subscribers"],
)


@router.post(
    path="/",
    response_model=Subscriber,
    description="Creates new subscriber",
    responses={409: {"description": "Subscriber exists"}},
)
async def create_subscriber(subscriber: SubscriberCreate, db: AsyncSession = Depends(get_db)):
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
async def update_user(user_id: int, user: SubscriberUpdate, db: AsyncSession = Depends(get_db)):
    model = await subscriber_service.get(session=db, id=user_id)
    if not model:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    await subscriber_service.update(session=db, db_obj=model, obj_in=user)
    return (await subscriber_service.get(session=db, id=user_id)).to_pd()


@router.delete(
    path="/{user_id}",
    response_model=SubscriberDeletedResponse,
    description="Deletes existing subscriber",
    responses={404: {"description": "Subscriber not found"}},
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    model = await subscriber_service.get(session=db, id=user_id)
    if not model:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    await subscriber_service.delete(session=db, id=user_id)
    return SubscriberDeletedResponse(id=user_id)
