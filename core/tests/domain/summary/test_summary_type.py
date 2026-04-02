from src.domain.summary import SummaryType


class TestSummaryType:
    def test_should_try_from(self):
        assert SummaryType.try_from('description') == SummaryType.DESCRIPTION
        assert SummaryType.try_from('biography') == SummaryType.BIOGRAPHY
        assert SummaryType.try_from('wrong') == SummaryType.DESCRIPTION
