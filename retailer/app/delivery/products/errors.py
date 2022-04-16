from app.base.errors import NotFoundError


class ProductNotFoundError(NotFoundError):
    def __init__(self, name: str):
        super().__init__(
            description=f"Product {name} not found",
        )
