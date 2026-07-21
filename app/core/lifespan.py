from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.database import connect_database, disconnect_database

@asynccontextmanager
async def lifespan(app: FastAPI): # Mandatory to keep this app parameter for fastapi

    # Startup

    await connect_database()

    yield

    #Shutdown

    await disconnect_database()