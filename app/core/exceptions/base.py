class AppException(Exception):
    status_code = 500
    message = "Internal server error"
    error_code = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str | None = None, error_code: str | None = None):
        self.message = message or self.message
        self.error_code = error_code or self.error_code