from sqlalchemy.orm import as_declarative
from app.store.pg.sa import metadata


@as_declarative(metadata=metadata)
class BaseModel:
    pass
