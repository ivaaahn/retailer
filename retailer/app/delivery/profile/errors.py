from app.base.errors import NotFoundError


class AddressesNotFoundError(NotFoundError):
    description = "User does not have any addresses"

    def __init__(self, user_id: int):
        super().__init__(data=dict(user_id=user_id))
