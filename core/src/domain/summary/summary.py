from __future__ import annotations

from dataclasses import dataclass

from src.domain.identity import Entity
from .exception import UrlRequiredError
from .summary_state import SummaryState
from .summary_type import SummaryType


@dataclass
class Summary(Entity):
    """
    Summary class representing a summary of a document or text.
    """
    url: str = None
    type: SummaryType = None
    state: SummaryState = None
    reason: str = None
    content: str = None

    @classmethod
    def create(
            cls,
            url: str,
            type_: SummaryType,
            created_by: str,
    ) -> Summary:
        """
        Factory method to create a new Summary instance.
        """
        cls.check(url)

        return cls(
            url=url,
            type=type_,
            state=SummaryState.PENDING,
            reason='',
            content='',
            created_by=created_by,
        )

    def completed(self, content: str):
        """
        Marks the summary as completed and sets the content.
        """
        self.state = SummaryState.COMPLETED
        self.reason = ''
        self.content = content

    def failed(self, reason: str):
        """
        Marks the summary as failed and clears the content.
        """
        self.state = SummaryState.FAILED
        self.reason = reason
        self.content = ''

    @staticmethod
    def check(url: str):
        """
        Validates the summary
        :raises UrlRequiredError: If the URL is invalid (empty or whitespace).
        """
        if not url or not url.strip():
            raise UrlRequiredError()
