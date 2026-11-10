from fastapi import FastAPI
from app.api.rooms import router as rooms_router
from api.bookings import router as booking_router


app = FastAPI(title="Booking API")

app.include_router(rooms_router)
app.include_router(booking_router)