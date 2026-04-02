import pytest

from src.application.summary.summarize import SummaryMake
from src.domain.summary.exception import SummaryNotFoundError
from tests.doubles.infrastructure.persistence import SummaryRepositoryStub
from tests.doubles.infrastructure.services import TextGeneratorStub
from tests.fixtures import Ref


class TestSummaryMake:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_summary = SummaryRepositoryStub()
        self.text_generator = TextGeneratorStub()

        self.maker = SummaryMake(
            repo_summary=self.repo_summary,
            text_generator=self.text_generator,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(SummaryNotFoundError):
            await self.maker.dispatch('non-existing-id')

        assert self.repo_summary.stored is None

    @pytest.mark.asyncio
    async def test_should_make_summary(self):
        summary = self.repo_summary.put(Ref.SummaryBiography)

        made_summary = await self.maker.dispatch(summary.id)

        assert made_summary.content == self.text_generator.text
        assert self.repo_summary.stored is not None
