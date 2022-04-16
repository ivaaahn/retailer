from sqlalchemy import inspect as sa_inspect
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import as_declarative

from store.pg.sa import metadata


class _Base:
    def as_dict(self) -> dict:
        custom = self._as_dict()

        if not custom:
            return {c.key: getattr(self, c.key) for c in sa_inspect(self).mapper.column_attrs}

        return custom

    def _as_dict(self) -> dict:
        return {}

    @classmethod
    def from_cursor(cls, c: CursorResult):
        c = c.first()
        return cls(**c) if c else None


@as_declarative(metadata=metadata)
class BaseModel(_Base):
    pass
