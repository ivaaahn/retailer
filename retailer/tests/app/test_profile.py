from dataclasses import asdict
from unittest.mock import AsyncMock

from app.dto.api.profile import (
    AddressAddDTO,
    ProfileUpdateReqDTO,
    UserAddressListDTO,
)
from app.dto.api.shop import ShopListPagingParams, ShopListRespDTO, ShopRespDTO
from app.dto.api.user import UserAddressDTO, UserRespDTO
from app.dto.db.products import DBShopProductListDTO
from app.dto.db.profile import DBAddressListDTO
from app.dto.db.user import DBUserDTO
from app.services import ProfileService
from app.services.shop import ShopsService
from pytest_mock import MockerFixture
from tests.builders.db.address import AddressBuilder
from tests.builders.db.shops import DBShopBuilder
from tests.builders.db.user import DBUserBuilder
from tests.constants import DEFAULT_DATETIME
from tests.mocks import ShopsRepoMock, UsersRepoMock
from tests.mocks.repo.products import ProductsRepoMock


class TestProfile:
    SHOP_ID_MOCKED = 1
    NEW_NAME_MOCKED = "Some new name"
    ADDRESS_ID_MOCKED = 1

    async def test_add_address(
        self,
        mocker: MockerFixture,
        profile_service: ProfileService,
        users_repo_mock: UsersRepoMock,
        default_active_user_api: UserRespDTO,
        default_address_to_build: AddressBuilder,
    ) -> None:
        new_address = default_address_to_build.build()
        requester = default_active_user_api
        users_repo_add_address_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="add_address",
            return_value=self.ADDRESS_ID_MOCKED,
        )

        expected = UserAddressDTO(address_id=self.ADDRESS_ID_MOCKED)
        received = await profile_service.add_address(
            user_id=requester.id, new_addr=AddressAddDTO(**asdict(new_address))
        )

        assert received == expected
        users_repo_add_address_mocked.assert_awaited_once_with(
            user_id=requester.id,
            city=new_address.city,
            street=new_address.street,
            house=new_address.house,
            entrance=new_address.entrance,
            floor=new_address.floor,
            flat=new_address.flat,
        )

    async def test_patch(
        self,
        mocker: MockerFixture,
        profile_service: ProfileService,
        users_repo_mock: UsersRepoMock,
        default_active_user_api: UserRespDTO,
        default_user_to_build: DBUserBuilder,
    ) -> None:
        requester = default_active_user_api
        repo_user = default_user_to_build.build()
        users_repo_update_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="update",
            return_value=repo_user,
        )

        expected = UserRespDTO(**asdict(repo_user))
        received = await profile_service.patch(
            email=requester.email,
            new_data=ProfileUpdateReqDTO(name=self.NEW_NAME_MOCKED),
        )

        assert received == expected
        users_repo_update_mocked.assert_awaited_once_with(
            email=requester.email, name=self.NEW_NAME_MOCKED
        )

    async def test_get_addresses(
        self,
        mocker: MockerFixture,
        profile_service: ProfileService,
        users_repo_mock: UsersRepoMock,
        default_active_user_api: UserRespDTO,
        default_address_to_build: AddressBuilder,
        default_address_list_built: DBAddressListDTO,
    ) -> None:
        repo_addresses = default_address_list_built
        requester = default_active_user_api
        users_repo_get_addresses_list_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="get_addresses_list",
            return_value=repo_addresses,
        )

        expected = UserAddressListDTO(**asdict(repo_addresses))
        received = await profile_service.get_addresses_list(requester.id)

        assert received == expected
        users_repo_get_addresses_list_mocked.assert_awaited_once_with(
            requester.id
        )
