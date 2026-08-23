from core.exceptions import ConflictException, ForbiddenException, UnauthorizedException


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


class InvalidEmailVerification(UnauthorizedException):
    def __init__(self, message: str = "Invalid or expired email verification token"):
        super().__init__(message=message)


class EmailAlreadyVerified(ConflictException):
    def __init__(self, message: str = "Email is already verified"):
        super().__init__(message=message)
