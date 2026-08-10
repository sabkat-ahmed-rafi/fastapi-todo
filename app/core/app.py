from fastapi import Depends, FastAPI

from core.exceptions import register_exception_handler
from modules.auth import verify_api_key
from .lifespan import lifespan
from .router_registry import register_routers


def create_app() -> FastAPI:

    app = FastAPI(
        lifespan = lifespan,
        dependencies=[Depends(verify_api_key)],
    )

    register_exception_handler(app)

    register_routers(app)

    return app