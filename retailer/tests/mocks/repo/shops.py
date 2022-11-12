import pytest

from app.base.repo import BasePgRepo
from app.dto.api.shop import ShopListPagingParams
from app.dto.db.shops import DBShopDTO, DBShopListDTO
from app.services.shop.interface import IShopsRepo
from store import PgAccessor
from store.pg.config import PgConfig


class ShopsRepoMock(IShopsRepo, BasePgRepo):
    async def get_shop(self, id: int) -> DBShopDTO | None:
        pass

    async def get_list(self, paging_params: ShopListPagingParams) -> DBShopListDTO:
        pass


@pytest.fixture
def shops_repo_mock() -> ShopsRepoMock:
    return ShopsRepoMock(PgAccessor(PgConfig()))
