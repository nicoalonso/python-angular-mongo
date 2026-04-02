import pytest

from src.application.summary.reader import SummaryRead
from src.domain.summary import Summary
from src.domain.summary.exception import SummaryNotFoundError
from tests.doubles.infrastructure.persistence import SummaryRepositoryStub
from tests.fixtures import Ref


class TestSummaryRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_summary = SummaryRepositoryStub()
        self.reader = SummaryRead(repo_summary=self.repo_summary)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(SummaryNotFoundError):
            await self.reader.dispatch('non-existing-id')

    @pytest.mark.asyncio
    async def test_should_read_summary(self):
        summary = self.repo_summary.put(Ref.SummaryDescription)

        obtained_summary = await self.reader.dispatch(summary.id)

        assert isinstance(obtained_summary, Summary)
