import pytest

from retailer.store import rmq_accessor
from retailer.store.rmq import RMQAccessor


@pytest.fixture
def rmq_store() -> RMQAccessor:
    return rmq_accessor()
