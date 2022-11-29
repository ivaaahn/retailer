from app.dto.api.products import CartProductDTO
from pydantic import BaseModel, Field


class CartRespDTO(BaseModel):
    products: list[CartProductDTO] = Field(
        title="Список добавленных продуктов"
    )
    total_price: float = Field(title="Общая сумма заказа")
