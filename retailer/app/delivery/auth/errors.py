from app.base.errors import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


class SignupSessionCreateTimeoutNotExpired(ConflictError):
    description = "Signup session timeout not expired yet"

    def __init__(self, seconds_left: int):
        super().__init__(data=dict(seconds_left=seconds_left))


class UserAlreadyExistsError(ConflictError):
    description = "User with this email already exist"

    def __init__(self, email: str):
        super().__init__(data=dict(email=email))


class SignupSessionExpiredError(ForbiddenError):
    description = "Session expired"


class IncorrectCredsError(UnauthorizedError):
    description = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class IncorrectLoginCredsError(IncorrectCredsError):
    description = "Incorrect email or password"


class IncorrectCodeError(IncorrectCredsError):
    description = "Bad code"

    def __init__(self, attempts_left: int):
        super().__init__(data=dict(attempts_left=attempts_left))


class InactiveAccountError(UnauthorizedError):
    description = "Inactive account"


class UserNotFoundError(NotFoundError):
    description = "User with this email not found"

    def __init__(self, email: str):
        super().__init__(data=dict(email=email))


class SessionNotFoundError(NotFoundError):
    description = "Session not found"
