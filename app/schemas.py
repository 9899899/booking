from pydantic import BaseModel, Field, ConfigDict, model_validator, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoomCreate(BaseModel):
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1, description="Capacity must be greater than or equal to 1")
    description: str | None = None


class RoomRead(RoomCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    client_contact: EmailStr

    @model_validator(mode="after")
    def validate_booking_dates(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


class BookingRead(BookingCreate):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)