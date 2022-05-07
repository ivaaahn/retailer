from app.base.errors import ConflictError


class ShopAmbiguity(ConflictError):
    def __init__(self):
        super().__init__(
            description="В корзине есть продукты из разных магазинов",
        )
