from fastapi import APIRouter, Depends

from shared.responses import ApiResponse

from ..dependencies import get_email_verification_service
from ..schemas import ResendVerificationRequest, VerifyEmailRequest
from ..services.email_verification import EmailVerificationService


router = APIRouter()


@router.post("/verify-email", response_model=ApiResponse[None])
async def verify_email(
    data: VerifyEmailRequest,
    email_verification_service: EmailVerificationService = Depends(
        get_email_verification_service
    ),
):
    await email_verification_service.verify_email(data)
    return ApiResponse(
        message="Email verified successfully",
        data=None,
    )


@router.post("/resend-verification", response_model=ApiResponse[None])
async def resend_verification(
    data: ResendVerificationRequest,
    email_verification_service: EmailVerificationService = Depends(
        get_email_verification_service
    ),
):
    await email_verification_service.resend_verification(data)
    return ApiResponse(
        message="If an account exists for this email, a verification link has been sent",
        data=None,
    )
