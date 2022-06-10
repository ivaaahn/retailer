from enum import Enum
from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class BaseError(HTTPException):
    code: int = 500
    description: str = "Internal server error"
    kind: str = "internal_server_error"
    data: dict | None = None
    headers: dict | None = None

    def __init__(
        self,
        code: int | None = None,
        description: str | None = None,
        kind: str | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=code or self.code,
            detail={
                "kind": kind or self.kind,
                "description": description or self.description,
                "data": data or self.data or {},
            },
            headers=headers or self.headers or {},
        )


class DatabaseError(BaseError):
    code = (HTTP_500_INTERNAL_SERVER_ERROR,)
    description = "Internal database error"
    kind = "internal_database_error"


class NotFoundError(BaseError):
    code = HTTP_404_NOT_FOUND
    description = "Not found error"
    kind = "not_found_error"


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


class ForbiddenError(BaseError):
    code = HTTP_403_FORBIDDEN
    description = "Forbidden"
    kind = "forbidden_error"


class BadRequestError(BaseError):
    code = HTTP_400_BAD_REQUEST
    description = "Bad request"
    kind = "bad_request_error"


class UnauthorizedError(BaseError):
    code = HTTP_401_UNAUTHORIZED
    description = "Unauthorized"
    kind = "unauthorized_error"


class ConflictError(BaseError):
    code = HTTP_409_CONFLICT
    description = "Conflict"
    kind = "conflict_error"
