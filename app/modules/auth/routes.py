from fastapi import APIRouter, Depends, Response

from .schemas import LoginRequest, LoginResponse, RegisterRequest
from .security import ACCESS_TOKEN_EXPIRE_MINUTES
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
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    result = await auth_service.login(data)
    response.set_cookie(
        key="access_token",
        value=result.token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return result


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    user: Users = Depends(get_current_active_user),
):
    return user
