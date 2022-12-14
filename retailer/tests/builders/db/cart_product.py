from retailer.app.dto.db.products import DBShopProductDTO
from retailer.tests.builders.db.common import BaseBuilder


class CartApiBuilder(BaseBuilder):
    def __init__(self):
        self._products: list[dict] = []
        self._total_price = 0.0

    def add_product(
        self, product: DBShopProductDTO, qty: int = 1
    ) -> "CartApiBuilder":
        self._total_price += qty * product.price
        self._products.append(
            {
                "product": {
                    "id": product.id,
                    "photo": product.photo,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category,
                    "availability": product.availability,
                },
                "qty": qty,
                "price": qty * product.price,
            }
        )
        return self

    def build_response(self) -> dict:
        return {
            "products": self._products,
            "total_price": self._total_price,
        }
