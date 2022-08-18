from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.services.user.logic import user_service
from src.app.services.user.schemes import User, UserCreate, UserDeletedResponse, UserUpdate
from src.core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={200: {"description": "sus"}}
)


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    model = await user_service.get_by_phone(db, user.phone)
    if model:
        raise HTTPException(status_code=409, detail="User with given phone exists")
    await user_service.create_user(db, user)
    return (await user_service.get_by_phone(db, user.phone)).to_pd()


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    model = await user_service.get(session=db, id=user_id)
    if not model:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.update(session=db, db_obj=model, obj_in=user)
    return (await user_service.get(session=db, id=user_id)).to_pd()


@router.delete("/{user_id}", response_model=UserDeletedResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    model = await user_service.get(session=db, id=user_id)
    if not model:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.delete(session=db, id=user_id)
    return UserDeletedResponse(id=user_id)
