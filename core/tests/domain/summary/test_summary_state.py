from src.domain.summary import SummaryState


class TestSummaryState:
    def test_should_run_when_try_from(self):
        assert SummaryState.try_from('pending') == SummaryState.PENDING
        assert SummaryState.try_from('completed') == SummaryState.COMPLETED
        assert SummaryState.try_from('failed') == SummaryState.FAILED
        assert SummaryState.try_from('invalid') == SummaryState.PENDING
