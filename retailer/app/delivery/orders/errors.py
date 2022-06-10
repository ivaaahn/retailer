from app.base.errors import BadRequestError, NotFoundError


class OrderNotFoundError(NotFoundError):
    description = "Order with this ID not found"

    def __init__(self, id: int):
        super().__init__(data=dict(id=id))


class NoProductsInCartError(BadRequestError):
    description = "No products in your cart!"


class ProductTemporarilyUnavailable(BadRequestError):
    description = "The product temporarily unavailable in the shop"

    def __init__(self, product_id: int, shop_id: int):
        super().__init__(data=dict(product_id=product_id, shop_id=shop_id))
