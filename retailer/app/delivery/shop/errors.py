from app.base.errors import NotFoundError


class ShopNotFoundError(NotFoundError):
    description = "Shop not found"

    def __init__(self, id: int):
        super().__init__(data=dict(shop_id=id))
