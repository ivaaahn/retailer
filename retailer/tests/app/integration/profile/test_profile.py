from dataclasses import asdict
from datetime import date

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.dto.db.profile import DBAddressDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.models.user_addresses import UserAddressModel
from retailer.app.models.users import UserModel
from retailer.tests.builders.db.address import AddressBuilder
from retailer.tests.builders.db.user import save_user


class TestProfile:
    URI = "api/profile"

    async def test_get_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_active_user: DBUserDTO,
        auth_headers_default: dict[str, str],
    ) -> None:
        new_name, new_birthday = "Дмитрий", date(2001, 11, 22).isoformat()
        async with engine.begin() as conn:
            default_active_user.id = await save_user(conn, default_active_user)

        expected_email = default_active_user.email
        expected_name = new_name
        expected_birthday = new_birthday

        response = await cli.patch(
            self.URI,
            json={"name": new_name, "birthday": new_birthday},
            headers=auth_headers_default,
        )
        assert response.is_success
        response_api = response.json()

        async with engine.begin() as conn:
            cursor = await conn.execute(
                select(UserModel).where(
                    UserModel.__table__.c.email == default_active_user.email
                )
            )
            response_db = cursor.first()

        received_email_api = response_api["email"]
        assert received_email_api == expected_email

        received_name_api = response_api["name"]
        assert received_name_api == expected_name

        received_name_db = response_db.name
        assert received_name_db == expected_name

        received_birthday_api = response_api["birthday"]
        assert received_birthday_api == expected_birthday

        received_birthday_db = response_db.birthday.isoformat()
        assert received_birthday_db == expected_birthday

    async def test_add_address_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_active_user: DBUserDTO,
        auth_headers_default: dict[str, str],
        default_address_to_build: AddressBuilder,
    ) -> None:
        new_address: DBAddressDTO = (
            default_address_to_build.but()
            .with_city("Москва")
            .with_street("7-я Парковая")
            .with_house("25А")
            .with_entrance(2)
            .with_floor(4)
            .with_flat("25")
            .build()
        )
        new_address_json = asdict(new_address)
        new_address_json.pop("id")

        async with engine.begin() as conn:
            user = await save_user(conn, default_active_user)

        response = await cli.put(
            f"{self.URI}/address",
            json=new_address_json,
            headers=auth_headers_default,
        )
        assert response.is_success
        response_api = response.json()

        async with engine.begin() as conn:
            cursor = await conn.execute(
                select(UserAddressModel).where(
                    UserAddressModel.__table__.c.user_id == user.id
                )
            )
        response_db = cursor.first()

        received_id_api = response_api["address_id"]
        received_id_db = response_db["id"]
        assert received_id_db == received_id_api

        response_db_map = dict(response_db)
        for key in ("id", "user_id"):
            response_db_map.pop(key)

        assert response_db_map == new_address_json
