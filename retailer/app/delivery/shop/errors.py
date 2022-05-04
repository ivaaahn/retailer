from app.base.errors import NotFoundError


class ShopNotFoundError(NotFoundError):
    def __init__(self, id: int):
        super().__init__(
            description=f"Shop {id} not found",
        )
