from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.database import connect_database, disconnect_database


@asynccontextmanager
async def lifespan(app: FastAPI): # Mandatory to keep this app parameter for fastapi

    # Startup
    # Ensure all models are imported so Base.metadata knows about them
    import users.model  # noqa: F401
    import modules.auth.models.email_verification_token  # noqa: F401
    import modules.auth.models.password_reset_code  # noqa: F401
    import modules.auth.models.refresh_token  # noqa: F401
    import modules.files.models  # noqa: F401

    await connect_database()

    yield

    #Shutdown

    await disconnect_database()