from typing import Optional

from pydantic import BaseModel, Field


class BaseProductRespDTO(BaseModel):
    name: str = Field(title="Название продукта")
    description: Optional[str] = Field(title="Описание продукта")
    category: str = Field(title="Категория продукта")
