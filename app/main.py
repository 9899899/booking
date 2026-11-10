from fastapi import FastAPI
from api.rooms import router as rooms_router


app = FastAPI(title="Booking API")

app.include_router(rooms_router)