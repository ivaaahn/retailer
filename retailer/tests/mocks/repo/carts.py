import pytest

from app.base.repo import BaseRedisRepo
from app.dto.db.products import DBCartInfoDTO, DBCartProductDTO
from app.services.carts.interfaces import ICartsRepo
from store.redis import RedisAccessor
from store.redis.config import RedisConfig


class CartsRepoMock(ICartsRepo, BaseRedisRepo):
    async def add_to_cart(self, email: str, dto: DBCartProductDTO) -> int:
        pass

    async def remove(self, email: str, product_id: int) -> int:
        pass

    async def get(self, email: str) -> DBCartInfoDTO:
        pass

    async def clear_cart(self, email: str) -> int:
        pass


@pytest.fixture
def carts_repo_mock() -> CartsRepoMock:
    return CartsRepoMock(RedisAccessor(RedisConfig()))
