from fastapi import APIRouter, Depends

from .schemas import LoginRequest, LoginResponse, RegisterRequest
from .service import AuthService
from .dependencies import get_auth_service, get_current_active_user
from users.schemas import UserResponse
from users.model import Users

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(data)


@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    user: Users = Depends(get_current_active_user),
):
    return user
