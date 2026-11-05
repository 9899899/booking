from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from sqlalchemy import text


app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db": "ok"}