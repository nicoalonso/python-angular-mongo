import pytest

from src.application.summary.creator import SummaryCreate, SummaryCreatePayload, SummaryCreatedEvent
from src.domain.summary import Summary, SummaryType
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.doubles.infrastructure.persistence import UserRepositoryStub, SummaryRepositoryStub
from tests.fixtures import Ref


class TestSummaryCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_summary = SummaryRepositoryStub()
        self.bus = DomainBusStub()
        repo_user = UserRepositoryStub()

        self.creator = SummaryCreate(
            repo_summary=self.repo_summary,
            repo_user=repo_user,
            bus=self.bus,
        )

        self.payload = SummaryCreatePayload(
            url='https://example.com/article',
            type='biography',
        )

    @pytest.mark.asyncio
    async def test_should_not_create_when_exists(self):
        self.repo_summary.put(Ref.SummaryDescription)

        summary = await self.creator.dispatch(self.payload)

        assert isinstance(summary, Summary)
        assert self.repo_summary.stored is None

    @pytest.mark.asyncio
    async def test_should_create_summary(self):
        summary = await self.creator.dispatch(self.payload)

        assert summary.url == self.payload.url
        assert summary.type == SummaryType.BIOGRAPHY
        assert self.repo_summary.stored is not None
        assert_dispatch(self.bus, SummaryCreatedEvent)
