from retailer.app.base.errors import NotFoundError


class ProductNotFoundError(NotFoundError):
    description = "The product not found"

    def __init__(self, product_id: int, shop_id: int):
        super().__init__(data=dict(product_id=product_id, shop_id=shop_id))
