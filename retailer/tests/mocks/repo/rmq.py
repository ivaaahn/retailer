import pytest
from app.base.repo import BaseRMQRepo
from app.services.auth.interfaces import IRMQInteractRepo
from store.rmq import RMQAccessor
from store.rmq.config import RMQConfig


class RMQInteractionRepoMock(IRMQInteractRepo, BaseRMQRepo):
    async def send_code(self, email: str, code: str):
        return None

    async def send_accept(self, email: str, order_id: int):
        return None


@pytest.fixture
def rmq_interaction_repo_mock() -> RMQInteractionRepoMock:
    return RMQInteractionRepoMock(RMQAccessor(RMQConfig()))
