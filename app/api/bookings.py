from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db import get_session
from app.models import Booking
from app.schemas import BookingCreate, BookingRead


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingRead)
async def create_booking(booking_in:BookingCreate, session: AsyncSession = Depends(get_session)):
        query = select(Booking).where(
                        and_(
                                Booking.room_id == booking_in.room_id,
                                Booking.start_time < booking_in.end_time,
                                Booking.end_time > booking_in.start_time
                        )
                )

        result = await session.execute(query)
        existing_booking = result.scalars().first()

        if existing_booking:
                raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Room is already booked for this time period"
                )

        new_booking = Booking(**booking_in.model_dump())
        session.add(new_booking)
        await session.commit()
        await session.refresh(new_booking)
        return new_booking


@router.get("", response_model=list[BookingRead])
async def get_bookings(session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(Booking))
        return result.scalars().all()