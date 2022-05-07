def make_cart_key(email: str) -> str:
    return f"cart:{email}"


def make_product_key(product_id: int) -> str:
    return f"product:{product_id}"


def make_shop_product_key(product_id: int, shop_id: int) -> str:
    return f"product:{product_id}:{shop_id}"


def parse_product_key(key: str) -> int:
    split = key.split(sep=":")
    return int(split[1])


def parse_shop_product_key(key: str) -> tuple[int, int]:
    split = key.split(sep=":")
    return int(split[1]), int(split[2])
