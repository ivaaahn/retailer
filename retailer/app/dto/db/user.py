from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.models.users import UserRolesEnum


@dataclass
class DBUserDTO:
    email: str
    password: str
    created_at: datetime
    is_active: bool
    name: str
    birthday: datetime
    last_login: datetime
    role: UserRolesEnum

    @classmethod
    def from_db(cls, db: Mapping | None) -> Optional["DBUserDTO"]:
        return cls(**db) if db else None
