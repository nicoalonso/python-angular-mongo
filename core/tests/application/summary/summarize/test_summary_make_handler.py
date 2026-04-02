import pytest

from src.application.summary.creator import SummaryCreatedEvent
from src.application.summary.summarize import SummaryMake, SummaryMakeHandler
from tests.doubles.infrastructure.persistence import SummaryRepositoryStub
from tests.doubles.infrastructure.services import TextGeneratorStub
from tests.fixtures import Ref


class TestSummaryMakeHandler:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_summary = SummaryRepositoryStub()
        self.text_generator = TextGeneratorStub()

        maker = SummaryMake(
            repo_summary=self.repo_summary,
            text_generator=self.text_generator,
        )
        self.handler = SummaryMakeHandler(maker)

    @pytest.mark.asyncio
    async def test_should_handle_summary_make(self):
        summary = self.repo_summary.put(Ref.SummaryBiography)

        event = SummaryCreatedEvent(summary.id)
        made_summary = await self.handler.handle(event)

        assert made_summary.content == self.text_generator.text
        assert self.repo_summary.stored is not None

    @pytest.mark.asyncio
    async def test_should_handle_summary_make_not_found(self):
        event = SummaryCreatedEvent('non-existing-id')
        await self.handler.handle(event)

        assert self.repo_summary.stored is None
