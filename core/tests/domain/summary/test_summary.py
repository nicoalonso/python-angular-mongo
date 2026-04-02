import pytest

from src.domain.summary import Summary, SummaryType, SummaryState
from src.domain.summary.exception import UrlRequiredError


class TestSummary:
    def test_should_fail_when_url_empty(self):
        with pytest.raises(UrlRequiredError):
            Summary.create(
                url='',
                type_=SummaryType.DESCRIPTION,
                created_by='test_user',
            )

    def test_should_run_when_create(self):
        summary = Summary.create(
            url='https://example.com/document',
            type_=SummaryType.DESCRIPTION,
            created_by='test_user',
        )

        assert summary.url == 'https://example.com/document'
        assert summary.type == SummaryType.DESCRIPTION
        assert summary.state == SummaryState.PENDING
        assert summary.reason == ''
        assert summary.content == ''

    def test_should_run_when_completed(self):
        summary = Summary.create(
            url='https://example.com/document',
            type_=SummaryType.DESCRIPTION,
            created_by='test_user',
        )

        summary.completed(content='This is a summary of the document.')

        assert summary.state == SummaryState.COMPLETED
        assert summary.reason == ''
        assert summary.content == 'This is a summary of the document.'

    def test_should_run_when_failed(self):
        summary = Summary.create(
            url='https://example.com/document',
            type_=SummaryType.DESCRIPTION,
            created_by='test_user',
        )

        summary.failed(reason='Failed to summarize the document.')

        assert summary.state == SummaryState.FAILED
        assert summary.reason == 'Failed to summarize the document.'
        assert summary.content == ''
