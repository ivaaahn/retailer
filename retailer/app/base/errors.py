from enum import Enum
from typing import Optional, Any

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


def check_err(err: IntegrityError, item: DBErrEnum):
    return item.value in str(err.orig)


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
        super(AuthError, self).__init__(
            code=status.HTTP_409_CONFLICT,
            description=description,
            kind=kind,
            data=data,
            headers=headers,
        )
