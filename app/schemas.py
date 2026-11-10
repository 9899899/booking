from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime


class RoomCreate(BaseModel):
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    description: str | None = None


class RoomRead(RoomCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    client_contact: str

    @model_validator(mode="after")
    def validate_booking_dates(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


class BookingRead(BookingCreate):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)