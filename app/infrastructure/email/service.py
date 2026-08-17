from functools import lru_cache
from html import escape
from pathlib import Path
from string import Template

from .client import EmailClient, EmailDelivery, EmailMessage
from .exceptions import EmailTemplateError


class EmailService:

    def __init__(self, client: EmailClient):
        self.client = client

    async def send(self, message: EmailMessage) -> EmailDelivery:
        return await self.client.send(message)

    async def send_password_reset(
        self,
        *,
        recipient: str,
        reset_code: str,
        recipient_name: str | None = None,
        expires_in_minutes: int = 30,
        idempotency_key: str | None = None,
    ) -> EmailDelivery:
        display_name = recipient_name or "there"
        html = self._render_template(
            "password_reset.html",
            {
                "recipient_name": display_name,
                "reset_code": reset_code,
                "expires_in_minutes": expires_in_minutes,
            },
        )
        text = (
            f"Hi {display_name},\n\n"
            f"Use this code to reset your password: {reset_code}\n\n"
            f"This code expires in {expires_in_minutes} minutes. If you did not "
            "request a password reset, you can ignore this email."
        )
        return await self.send(
            EmailMessage(
                recipients=(recipient,),
                subject="Reset your password",
                html=html,
                text=text,
                idempotency_key=idempotency_key,
            )
        )

    @staticmethod
    @lru_cache(maxsize=8)
    def _load_template(template_name: str) -> Template:
        template_path = Path(__file__).parent / "templates" / template_name
        try:
            return Template(template_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EmailTemplateError(f"Email template not found: {template_name}") from exc

    @classmethod
    def _render_template(cls, template_name: str, context: dict[str, object]) -> str:
        escaped_context = {
            key: escape(str(value), quote=True)
            for key, value in context.items()
        }
        try:
            return cls._load_template(template_name).substitute(escaped_context)
        except (KeyError, ValueError) as exc:
            raise EmailTemplateError() from exc
