from core.exceptions import AppException
from core.exceptions.codes import ErrorCode


class UserNotFound(AppException):
    def __init__(self, message: str = "User not found"):
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
        )


class EmailAlreadyExists(AppException):
    def __init__(self, message: str = "Email already exists"):
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFLICT,
            status_code=409,
        )
