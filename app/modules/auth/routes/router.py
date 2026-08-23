from fastapi import APIRouter

from .email_verification import router as email_verification_router
from .password_reset import router as password_reset_router
from .registration import router as registration_router
from .session import router as session_router


router = APIRouter()
router.include_router(registration_router)
router.include_router(session_router)
router.include_router(password_reset_router)
router.include_router(email_verification_router)
