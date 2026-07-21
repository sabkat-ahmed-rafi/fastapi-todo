from fastapi import FastAPI
from core.exceptions import register_exception_handler
from .lifespan import lifespan



def create_app() -> FastAPI:

    app = FastAPI(
        lifespan = lifespan
    )

    register_exception_handler(app)

    return app