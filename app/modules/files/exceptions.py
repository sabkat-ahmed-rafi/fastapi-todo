from core.exceptions import AppException
from core.exceptions.codes import ErrorCode


class InvalidFileType(AppException):
    def __init__(self, message: str = "Invalid file type"):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=422,
        )


class FileTooLarge(AppException):
    def __init__(self, message: str = "File too large"):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=422,
        )


class FileNotFound(AppException):
    def __init__(self, message: str = "File not found"):
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
        )
