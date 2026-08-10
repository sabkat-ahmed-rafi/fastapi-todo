from fastapi import FastAPI

from core.exceptions import register_exception_handler
from modules.auth.routes import router as auth_router
from .lifespan import lifespan



def create_app() -> FastAPI:

    app = FastAPI(
        lifespan = lifespan
    )

    register_exception_handler(app)

    app.include_router(auth_router)

    return app