from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from tests.constants import DEFAULT_S3_URL


@pytest.fixture
def make_s3_url_mocked(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        target="app.services.ProductsService._make_s3_url",
        return_value=DEFAULT_S3_URL,
    )
