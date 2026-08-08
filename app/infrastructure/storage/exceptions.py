from core.exceptions import AppException
from core.exceptions.codes import ErrorCode


class StorageFileNotFound(AppException):
    def __init__(self, message: str = "File not found in storage"):
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
        )


class UploadFailed(AppException):
    def __init__(self, message: str = "Upload failed"):
        super().__init__(
            message=message,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=500,
        )
