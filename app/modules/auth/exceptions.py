from core.exceptions import UnauthorizedException, ForbiddenException


class InvalidCredentials(UnauthorizedException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message)


class TokenExpired(UnauthorizedException):
    def __init__(self, message: str = "Token expired"):
        super().__init__(message=message)


class InactiveUser(ForbiddenException):
    def __init__(self, message: str = "Inactive user"):
        super().__init__(message=message)


class InvalidPasswordReset(UnauthorizedException):
    def __init__(self, message: str = "Invalid or expired password reset credentials"):
        super().__init__(message=message)
