# core/router_registry.py
from fastapi import APIRouter, FastAPI
from modules.auth import auth_router


def register_routers(app: FastAPI, base_prefix: str = "/api"):

    api_router = APIRouter(prefix=base_prefix)
    
    # Register routers
    api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    
    app.include_router(api_router)
    return app