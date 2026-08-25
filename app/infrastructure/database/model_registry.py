"""Import every SQLAlchemy model so its table is registered on Base.metadata."""

from infrastructure.database.base import Base
from modules.auth.models.email_verification_token import EmailVerificationToken
from modules.auth.models.password_reset_code import PasswordResetCode
from modules.auth.models.refresh_token import RefreshToken
from modules.files.models import File
from modules.users.model import Users


# Keeping explicit references documents the complete model registry and prevents
# static analysis tools from treating these registration imports as unused.
REGISTERED_MODELS = (
    Users,
    File,
    RefreshToken,
    PasswordResetCode,
    EmailVerificationToken,
)

model_metadata = Base.metadata
