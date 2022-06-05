import random
from dataclasses import dataclass

from scripts.faker.rw import write

FILENAME_SHOP_PRODUCTS = "data/shop_products.csv"
NUMBER_OF_PRODUCTS_IN_DB = 1108
NUMBER_OF_SHOPS_IN_DB = 1000


def _get_random_price() -> float:
    return float(random.randint(50, 1000))


def _get_random_qty() -> int:
    return random.randint(100, 1000)


@dataclass
class ShopProduct:
    shop_id: int
    product_id: int
    qty: int
    price: float


def _generate_shop_product(shop_id: int, product_id: int) -> ShopProduct:
    return ShopProduct(
        shop_id=shop_id,
        product_id=product_id,
        qty=_get_random_qty(),
        price=_get_random_price(),
    )


def _generate_shop_products() -> list[ShopProduct]:
    result: list[ShopProduct] = []

    for shop_id in range(1, NUMBER_OF_SHOPS_IN_DB + 1):
        for product_id in range(1, NUMBER_OF_PRODUCTS_IN_DB + 1):
            result.append(_generate_shop_product(shop_id, product_id))

    return result


def generate(to_file: bool = False) -> list[ShopProduct]:
    shop_products = _generate_shop_products()

    if to_file:
        write(shop_products, FILENAME_SHOP_PRODUCTS)

    return shop_products


if __name__ == "__main__":
    generate()
