from app.base.errors import NotFoundError


class OrderNotFoundError(NotFoundError):
    def __init__(self, id: int):
        super().__init__(
            description=f"Order {id} not found",
        )
