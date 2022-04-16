from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProfileUpdateReqDTO(BaseModel):
    name: Optional[str]
    birthday: Optional[date]
