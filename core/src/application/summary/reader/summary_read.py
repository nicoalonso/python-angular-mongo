from src.domain.summary import Summary, SummaryRepository
from src.domain.summary.exception import SummaryNotFoundError


class SummaryRead:
    """
    Use case for reading a summary.
    """
    def __init__(self, repo_summary: SummaryRepository):
        self.repo_summary = repo_summary

    async def dispatch(self, summary_id: str) -> Summary:
        """
        Dispatch the use case to read a summary by its ID.
        :param summary_id: Summary ID to read.
        :return: The summary object.
        """
        summary = await self.repo_summary.obtain_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(summary_id)

        return summary
