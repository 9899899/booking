from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings


async_engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commite=False,
    class_=AsyncSession
)


async def get_session():
    async with async_session() as session:
        yield session