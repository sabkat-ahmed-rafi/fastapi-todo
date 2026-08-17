from core.config import settings

from .client import EmailClient
from .exceptions import EmailConfigurationError
from .providers import ResendEmailClient
from .service import EmailService


def get_email_client() -> EmailClient:
    if settings.EMAIL_PROVIDER == "resend":
        return ResendEmailClient(
            api_key=settings.RESEND_API_KEY,
            sender=settings.EMAIL_FROM,
        )
    raise EmailConfigurationError(
        f"Unsupported email provider: {settings.EMAIL_PROVIDER}"
    )


def get_email_service() -> EmailService:
    return EmailService(client=get_email_client())
