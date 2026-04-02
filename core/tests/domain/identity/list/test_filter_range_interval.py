from src.domain.identity.list.filter_range_interval import FilterRangeInterval


class TestFilterRangeInterval:
    def test_should_false_when_value_is_not_a_list(self):
        (name, interval) = FilterRangeInterval.check('name')

        assert name == 'name'
        assert interval == FilterRangeInterval.Empty

    def test_should_range_from_when_value_has_prefix(self):
        (name, interval) = FilterRangeInterval.check('fromName')

        assert name == 'name'
        assert interval == FilterRangeInterval.From

    def test_should_range_to_when_value_has_prefix(self):
        (name, interval) = FilterRangeInterval.check('toName')

        assert name == 'name'
        assert interval == FilterRangeInterval.To
