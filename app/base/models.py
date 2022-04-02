from typing import Optional

from sqlalchemy import inspect
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import as_declarative
from app.store.pg.sa import metadata


class _Base:
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def from_cursor(cls, c: CursorResult):
        c = c.first()
        return cls(**c) if c else None


@as_declarative(metadata=metadata)
class BaseModel(_Base):
    pass
