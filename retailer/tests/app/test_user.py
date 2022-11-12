from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import EmailStr
from pytest_mock import MockerFixture

from app.dto.api.signup import SignupRespDTO, TokenRespDTO
from app.dto.db.signup_session import DBSignupSessionDTO
from app.dto.db.user import DBUserDTO
from app.services import AuthService
from tests.builders.db.signup_session import DBSignupSessionBuilder
from tests.builders.db.user import DBUserBuilder
from tests.constants import (
    DEFAULT_DATETIME,
    DEFAULT_JWT_ACCESS_TOKEN,
    DEFAULT_PASSWORD,
)
from tests.mocks import RMQInteractionRepoMock
from tests.mocks.repo.signup_session import SignupSessionRepoMock
from tests.mocks.repo.user import UsersRepoMock


class TestUser:
    @pytest.mark.usefixtures("patch_auth_service")
    @pytest.mark.freeze_time(DEFAULT_DATETIME)
    async def test_signup(
        self,
        mocker: MockerFixture,
        users_repo_mock: UsersRepoMock,
        signup_session_repo_mock: SignupSessionRepoMock,
        rmq_interaction_repo_mock: RMQInteractionRepoMock,
        default_user_to_build: DBUserBuilder,
        default_signup_session_to_build: DBSignupSessionBuilder,
        auth_get_password_hash_mocked: MagicMock,
        auth_service: AuthService,
    ) -> None:
        test_user: DBUserDTO = default_user_to_build.build()
        test_signup_session: DBSignupSessionDTO = (
            default_signup_session_to_build.build()
        )
        email, pswd_hashed, code, attempts_left = (
            test_user.email,
            test_user.password,
            test_signup_session.code,
            test_signup_session.attempts_left,
        )

        users_repo_upsert_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="upsert",
            return_value=test_user,
        )
        ss_repo_upsert_mocked: AsyncMock = mocker.patch.object(
            target=signup_session_repo_mock,
            attribute="upsert",
            return_value=test_signup_session,
        )
        send_code_to_rmq_mocked: AsyncMock = mocker.spy(
            obj=rmq_interaction_repo_mock,
            name="send_code",
        )
        expected = SignupRespDTO(email=EmailStr(email), seconds_left=60)
        received = await auth_service.signup_user(email, DEFAULT_PASSWORD)

        assert received == expected
        send_code_to_rmq_mocked.assert_awaited_once_with(email, code)
        users_repo_upsert_mocked.assert_awaited_once_with(email, pswd_hashed)
        ss_repo_upsert_mocked.assert_awaited_once_with(email, code)
        auth_get_password_hash_mocked.assert_called_once_with(DEFAULT_PASSWORD)

    @pytest.mark.usefixtures("patch_auth_service")
    async def test_verify_code(
        self,
        mocker: MockerFixture,
        users_repo_mock: UsersRepoMock,
        signup_session_repo_mock: SignupSessionRepoMock,
        default_active_user_to_build: DBUserBuilder,
        default_attempt_wasted_signup_session_to_build: DBSignupSessionBuilder,
        auth_service: AuthService,
    ) -> None:
        test_user: DBUserDTO = default_active_user_to_build.build()
        test_signup_session: DBSignupSessionDTO = (
            default_attempt_wasted_signup_session_to_build.build()
        )
        email, pswd_hashed, code, attempts_left = (
            test_user.email,
            test_user.password,
            test_signup_session.code,
            test_signup_session.attempts_left,
        )
        ss_repo_waste_attempt_mocked: AsyncMock = mocker.patch.object(
            target=signup_session_repo_mock,
            attribute="waste_attempt",
            return_value=test_signup_session,
        )

        users_repo_update_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="update",
            return_value=test_user,
        )

        received = await auth_service.verify_code(email, code)
        expected = email

        assert received == expected
        ss_repo_waste_attempt_mocked.assert_awaited_once_with(email)
        users_repo_update_mocked.assert_awaited_once_with(email, is_active=True)

    @pytest.mark.freeze_time(DEFAULT_DATETIME)
    @pytest.mark.usefixtures("patch_auth_service")
    async def test_login(
        self,
        mocker: MockerFixture,
        users_repo_mock: UsersRepoMock,
        default_active_user_to_build: DBUserBuilder,
        auth_verify_pass_mocked: MagicMock,
        jwt_encode_mocked: MagicMock,
        jwt_encode_call_args_default: dict,
        auth_service: AuthService,
    ) -> None:
        test_user: DBUserDTO = default_active_user_to_build.build()
        email, pass_hash = test_user.email, test_user.password

        users_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="get",
            return_value=test_user,
        )
        users_repo_update_mocked: AsyncMock = mocker.patch.object(
            target=users_repo_mock,
            attribute="update",
        )

        received = await auth_service.login_user(email, DEFAULT_PASSWORD)
        expected = TokenRespDTO(
            access_token=DEFAULT_JWT_ACCESS_TOKEN,
            token_type="bearer",
        )

        assert received == expected
        users_repo_get_mocked.assert_awaited_once_with(email, only_active=False)
        users_repo_update_mocked.assert_awaited_once_with(
            email, last_login=DEFAULT_DATETIME
        )
        auth_verify_pass_mocked.assert_called_once_with(DEFAULT_PASSWORD, pass_hash)
        jwt_encode_mocked.assert_called_once_with(**jwt_encode_call_args_default)
