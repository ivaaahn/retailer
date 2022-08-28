from app.base.repo import BaseRedisRepo
from app.dto.db.products import DBCartProductDTO, DBCartInfoDTO
from app.misc import make_cart_key, make_product_key, parse_product_key


class CartsRepo(BaseRedisRepo):
    async def add_to_cart(self, email: str, dto: DBCartProductDTO) -> int:
        return await self._redis.cli.hset(
            name=make_cart_key(email),
            key=make_product_key(dto.product_id),
            value=dto.qty,
        )

    async def remove(self, email: str, product_id: int) -> int:
        return await self._redis.cli.hdel(
            make_cart_key(email), make_product_key(product_id)
        )

    async def get(self, email: str) -> DBCartInfoDTO:
        products_raw: dict = await self._redis.cli.hgetall(
            name=make_cart_key(email),
        )

        products = [
            DBCartProductDTO(
                product_id=parse_product_key(p_key),
                qty=int(p_value),
            )
            for p_key, p_value in products_raw.items()
        ]

        return DBCartInfoDTO(products=products)

    async def clear_cart(self, email: str) -> int:
        return await self._redis.cli.delete(make_cart_key(email))
