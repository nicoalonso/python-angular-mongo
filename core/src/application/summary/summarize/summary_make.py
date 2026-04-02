import logging

from src.domain.summary import SummaryRepository, TextGenerator, Summary
from src.domain.summary.exception import SummaryNotFoundError


class SummaryMake:
    """
    Use case for creating a summary

    :ivar repo_summary: SummaryRepository
    :ivar text_generator: TextGenerator
    :ivar log: logging.Logger
    """
    def __init__(
            self,
            repo_summary: SummaryRepository,
            text_generator: TextGenerator,
    ):
        self.repo_summary = repo_summary
        self.text_generator = text_generator
        self.log = logging.getLogger('uvicorn')

    async def dispatch(self, summary_id: str) -> Summary:
        """
        Generates a summary for the given summary ID.
        :param summary_id: Summary ID for which to generate the summary
        """
        summary = await self.repo_summary.obtain_by_id(summary_id)
        if summary is None:
            self.log.error(f"Summary with ID {summary_id} not found")
            raise SummaryNotFoundError(summary_id)

        self.log.info(f"Generating summary for URL: {summary.url}")
        generated_text = self.text_generator.generate(summary)
        self.log.info(f"Summary generated successfully: {generated_text}")
        summary.completed(generated_text)

        await self.repo_summary.save(summary)
        return summary
