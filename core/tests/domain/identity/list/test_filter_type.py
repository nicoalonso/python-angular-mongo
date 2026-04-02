from src.domain.identity.list import FilterType

class TestFilterType:
    def test_filter_type(self):
        assert FilterType.check(FilterType.Wildcard) == True
        assert FilterType.check("ft:wildcard") == True
        assert FilterType.check("wrong_filter") == False

    def test_is_value_list(self):
        assert FilterType.Wildcard.is_value_list() == False
        assert FilterType.Match.is_value_list() == False
        assert FilterType.Fuzzy.is_value_list() == False
        assert FilterType.Range.is_value_list() == False
        assert FilterType.In.is_value_list() == True
        assert FilterType.All.is_value_list() == True
        assert FilterType.Exists.is_value_list() == False
