from app.base.errors import NotFoundError


class AddressesNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__(
            description=f"User-{user_id} does not have any addresses",
        )
