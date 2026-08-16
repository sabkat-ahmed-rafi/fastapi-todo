from fastapi import APIRouter, Depends, Response

from shared.responses import ApiResponse
from .schemas import LoginRequest, LoginResponse, RegisterRequest, Token
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from .service import AuthService
from .dependencies import get_auth_service, get_current_active_user, verify_refresh_token
from users.schemas import UserResponse
from users.model import Users

router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse])
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.register(data)
    return ApiResponse(
        message="User registered successfully",
        data=user,
    )


@router.post("/login", response_model=ApiResponse[LoginResponse])
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
    response.set_cookie(
        key="refresh_token",
        value=result.token.refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return ApiResponse(
        message="Login successful",
        data=result,
    )


@router.post("/refresh", response_model=ApiResponse[Token])
async def refresh_access_token(
    response: Response,
    verified_token: tuple[str, dict] = Depends(verify_refresh_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    raw_token, payload = verified_token
    token = await auth_service.rotate_refresh_token(raw_token, payload)
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return ApiResponse(
        message="Tokens refreshed successfully",
        data=token,
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current_user_profile(
    user: Users = Depends(get_current_active_user),
):
    return ApiResponse(
        message="User profile fetched successfully",
        data=user,
    )
