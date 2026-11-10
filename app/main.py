from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from sqlalchemy import text, select
from app.models import Room
from app.schemas import RoomCreate, RoomRead


app = FastAPI(title="Booking API")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db": "ok"}


@app.post("/rooms", response_model=RoomRead)
async def create_room(room_in: RoomCreate, session: AsyncSession = Depends(get_session)):
    new_room = Room(**room_in.model_dump())
    session.add(new_room)
    await session.commit()
    await session.refresh(new_room)
    return new_room


@app.get("/rooms", response_model=list[RoomRead])
async def get_rooms(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Room))
    return result.scalars().all()