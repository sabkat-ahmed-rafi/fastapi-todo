from fastapi import FastAPI

from core.exceptions import register_exception_handler
from .lifespan import lifespan
from .router_registry import register_routers


def create_app() -> FastAPI:

    app = FastAPI(
        lifespan = lifespan
    )

    register_exception_handler(app)

    register_routers(app)

    return app