from app.base.errors import NotFoundError, BadRequestError


class OrderNotFoundError(NotFoundError):
    def __init__(self, id: int):
        super().__init__(
            description=f"Order {id} not found",
        )


class OrdersNotFoundError(NotFoundError):
    def __init__(self, id: int):
        super().__init__(
            description=f" User-{id} does not have any orders",
        )


class NoProductsInCartError(BadRequestError):
    def __init__(self):
        super().__init__(description="No products in your cart!")


class ProductTemporarilyUnavailable(BadRequestError):
    def __init__(self, product_id: int, shop_id: int):
        super().__init__(
            description=f"Продукт {product_id} временно не доступен в магазине {shop_id}"
        )
