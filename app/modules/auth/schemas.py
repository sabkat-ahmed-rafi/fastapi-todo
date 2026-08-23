from pydantic import BaseModel, EmailStr, Field

from users.schemas import UserResponse


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None


class LoginResponse(BaseModel):
    user: UserResponse
    token: Token


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyPasswordResetCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")


class PasswordResetAuthorization(BaseModel):
    reset_token: str
    expires_in_seconds: int


class ResetPasswordRequest(BaseModel):
    reset_token: str = Field(min_length=32)
    new_password: str = Field(min_length=8, max_length=72)


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=32)


class ResendVerificationRequest(BaseModel):
    email: EmailStr
