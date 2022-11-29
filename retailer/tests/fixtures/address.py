import pytest
from app.dto.db.profile import DBAddressListDTO
from tests.builders.db.address import AddressBuilder


@pytest.fixture
def default_address_to_build() -> AddressBuilder:
    return AddressBuilder()


@pytest.fixture
def default_address_list_built(
    default_address_to_build: AddressBuilder,
) -> DBAddressListDTO:
    qty = 2
    addresses = [
        default_address_to_build.but().with_id(idx).build()
        for idx in range(1, qty + 1)
    ]

    return DBAddressListDTO(addresses=addresses)
