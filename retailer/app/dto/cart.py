from pydantic import BaseModel, Field

from app.dto.products import CartProductDTO


class CartRespDTO(BaseModel):
    products: list[CartProductDTO] = Field(title="Список добавленных продуктов")
    total_price: float = Field(title="Общая сумма заказа")
