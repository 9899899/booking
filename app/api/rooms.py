from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.db import get_session
from app.models import Room
from app.schemas import RoomCreate, RoomRead


router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("", response_model=RoomRead)
async def create_room(room_in: RoomCreate, session: AsyncSession = Depends(get_session)):
    new_room = Room(**room_in.model_dump())
    session.add(new_room)
    await session.commit()
    await session.refresh(new_room)
    return new_room


@router.get("", response_model=list[RoomRead])
async def get_rooms(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Room))
    return result.scalars().all()