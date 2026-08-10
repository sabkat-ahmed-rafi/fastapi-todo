from core.exceptions import AppException
from core.exceptions.codes import ErrorCode


class InvalidCredentials(AppException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=401,
        )


class TokenExpired(AppException):
    def __init__(self, message: str = "Token expired"):
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=401,
        )


class InactiveUser(AppException):
    def __init__(self, message: str = "Inactive user"):
        super().__init__(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            status_code=403,
        )
