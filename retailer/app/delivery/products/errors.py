from app.base.errors import NotFoundError


class ProductNotFoundError(NotFoundError):
    def __init__(self, product_id: int, shop_id: int):
        super().__init__(
            description=f"Product {product_id} from {shop_id} shop not found",
        )
