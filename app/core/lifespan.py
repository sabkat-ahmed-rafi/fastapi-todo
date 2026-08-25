from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.database import disconnect_database


@asynccontextmanager
async def lifespan(app: FastAPI): # Mandatory to keep this app parameter for fastapi
    yield

    await disconnect_database()
