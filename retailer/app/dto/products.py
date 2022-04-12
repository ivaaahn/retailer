from typing import Optional

from pydantic import BaseModel, Field


class BaseProductDTO(BaseModel):
    name: str = Field(title="Название продукта")
    description: Optional[str] = Field(title="Описание продукта")
    category: str = Field(title="Категория продукта")
