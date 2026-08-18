from fastapi import APIRouter, Depends, Response

from shared.responses import ApiResponse
from .schemas import (
    AccessToken,
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    PasswordResetAuthorization,
    RegisterRequest,
    ResetPasswordRequest,
    VerifyPasswordResetCodeRequest,
)
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from .services.password_reset import PasswordResetService
from .services.registration import RegistrationService
from .services.session import SessionService
from .dependencies import (
    get_current_active_user,
    get_password_reset_service,
    get_registration_service,
    get_session_service,
    verify_refresh_token,
)
from users.schemas import UserResponse
from users.model import Users

router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse])
async def register(
    data: RegisterRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    user = await registration_service.register(data)
    return ApiResponse(
        message="User registered successfully",
        data=user,
    )


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(
    data: LoginRequest,
    response: Response,
    session_service: SessionService = Depends(get_session_service),
):
    result = await session_service.login(data)
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


@router.post("/refresh", response_model=ApiResponse[AccessToken])
async def refresh_access_token(
    response: Response,
    verified_token: tuple[str, dict] = Depends(verify_refresh_token),
    session_service: SessionService = Depends(get_session_service),
):
    raw_token, payload = verified_token
    access_token = await session_service.refresh_access_token(raw_token, payload)
    response.set_cookie(
        key="access_token",
        value=access_token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return ApiResponse(
        message="Access token refreshed successfully",
        data=access_token,
    )


@router.post("/logout", response_model=ApiResponse[None])
async def logout(
    response: Response,
    verified_token: tuple[str, dict] = Depends(verify_refresh_token),
    session_service: SessionService = Depends(get_session_service),
):
    raw_token, payload = verified_token
    await session_service.logout(raw_token, payload)
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return ApiResponse(
        message="Logout successful",
        data=None,
    )


@router.post("/forgot-password", response_model=ApiResponse[None])
async def forgot_password(
    data: ForgotPasswordRequest,
    password_reset_service: PasswordResetService = Depends(get_password_reset_service),
):
    await password_reset_service.request_reset(data)
    return ApiResponse(
        message="If an account exists for this email, a reset code has been sent",
        data=None,
    )


@router.post(
    "/verify-password-reset-code",
    response_model=ApiResponse[PasswordResetAuthorization],
)
async def verify_password_reset_code(
    data: VerifyPasswordResetCodeRequest,
    password_reset_service: PasswordResetService = Depends(get_password_reset_service),
):
    authorization = await password_reset_service.verify_code(data)
    return ApiResponse(
        message="Password reset code verified successfully",
        data=authorization,
    )


@router.post("/reset-password", response_model=ApiResponse[None])
async def reset_password(
    data: ResetPasswordRequest,
    response: Response,
    password_reset_service: PasswordResetService = Depends(get_password_reset_service),
):
    await password_reset_service.reset_password(data)
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return ApiResponse(
        message="Password reset successfully",
        data=None,
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current_user_profile(
    user: Users = Depends(get_current_active_user),
):
    return ApiResponse(
        message="User profile fetched successfully",
        data=user,
    )
