from enum import Enum
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status


class BaseError(HTTPException):
    def __init__(
        self,
        code: int,
        description: str,
        kind: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=code,
            detail={
                "type": kind or self.__class__.__name__,
                "description": description,
                "data": data or {},
            },
            headers=headers,
        )


class PostgresError(BaseError):
    def __init__(
        self,
        description: str,
        kind: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class NotFoundError(BaseError):
    def __init__(
        self,
        description: str,
        kind: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            code=status.HTTP_404_NOT_FOUND,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class DBErrEnum(str, Enum):
    foreign_key_violation = "ForeignKeyViolationError"
    check_violation = "CheckViolationError"


def check_err(
    err: IntegrityError,
    exp_error: DBErrEnum,
    raise_exc: Exception,
    default_exc: Exception | None = None,
):
    if exp_error in str(err.orig):
        raise raise_exc

    if default_exc:
        raise default_exc


class AuthError(BaseError):
    def __init__(
        self,
        code: int,
        description: str,
        kind: str = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super(AuthError, self).__init__(
            code=code,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class ForbiddenError(AuthError):
    def __init__(
        self,
        description: str,
        kind: str = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super(AuthError, self).__init__(
            code=status.HTTP_403_FORBIDDEN,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class BadRequestError(BaseError):
    def __init__(
        self,
        description: str,
        kind: str = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            code=status.HTTP_400_BAD_REQUEST,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class UnauthorizedError(AuthError):
    def __init__(
        self,
        description: str,
        kind: str = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super(AuthError, self).__init__(
            code=status.HTTP_401_UNAUTHORIZED,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )


class ConflictError(BaseError):
    def __init__(
        self,
        description: str,
        kind: str = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            code=status.HTTP_409_CONFLICT,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )
