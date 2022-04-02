from typing import Optional, Any

from starlette import status

from base.errors import NotFoundError, AuthError, ForbiddenError, UnauthorizedError


class AuthConflictError(AuthError):
    def __init__(self, description: str, data: Optional[dict[str, Any]] = None):
        super().__init__(
            code=status.HTTP_409_CONFLICT,
            description=description,
            data=data,
        )


class SignupSessionCreateTimeoutNotExpired(AuthConflictError):
    def __init__(self, seconds_left: int):
        super().__init__(
            description="Signup session timeout not expired yet",
            data={
                "seconds_left": seconds_left,
            },
        )


class UserAlreadyExistsError(AuthConflictError):
    def __init__(self, email: str):
        super().__init__(
            description=f"User with email {email} already exist",
            data={
                "email": email,
            },
        )


class SessionExpiredError(ForbiddenError):
    def __init__(self):
        super().__init__(description="Session not expired")


class IncorrectCredsError(UnauthorizedError):
    def __init__(self, description: str = "Could not validate credentials"):
        super().__init__(
            description=description,
            headers={"WWW-Authenticate": "Bearer"},
        )


class IncorrectLoginCredsError(IncorrectCredsError):
    def __init__(self):
        super().__init__(description="Incorrect email or password")


class IncorrectCodeError(IncorrectCredsError):
    def __init__(self, attempts_left: int):
        super().__init__(
            description=f"Bad code. You have {attempts_left} attempts yet!"
        )


class InactiveAccountError(UnauthorizedError):
    def __init__(self):
        super().__init__(
            description="Inactive account",
        )


# TODO вынести как более общую ошибку
class UserNotFoundError(NotFoundError):
    def __init__(self, email: str):
        super().__init__(
            description=f"User with email {email} not found",
            data={
                "email": email,
            },
        )


class SessionNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(
            description="Session not found",
        )
