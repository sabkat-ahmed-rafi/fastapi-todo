from pydantic import BaseModel

from users.schemas import UserResponse


class Token(BaseModel):
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
