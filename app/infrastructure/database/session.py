from sqlalchemy.ext.asyncio import ( 
    create_async_engine,
    async_sessionmaker,
)
from core.config import settings




engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True # It logs every sql query of sqlalchemy. Just for development/learning
)

SessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit = False
)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def connect_database():
    from .base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def disconnect_database():
    await engine.dispose()