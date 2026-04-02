from src.domain.identity.list import FilterRange, ValueKind


class TestFilterRange:
    def test_should_create_as_empty(self):
        filter_range = FilterRange()

        assert filter_range.has_value() is False
        assert filter_range.has_from() is False
        assert filter_range.has_to() is False
        assert filter_range.kind == ValueKind.String

    def test_should_has_value_when_has_one_value(self):
        filter_range = FilterRange(from_='test')

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is False

    def test_should_empty_when_empty_and_parse_as_date(self):
        filter_range = FilterRange()

        filter_range.parse(ValueKind.Date)

        assert filter_range.has_value() is False
        assert filter_range.has_from() is False
        assert filter_range.has_to() is False

    def test_should_run_when_create_with_values(self):
        filter_range = FilterRange(from_='10', to='50')

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.String
        assert filter_range.from_ == '10'
        assert filter_range.to == '50'

    def test_should_run_when_parse_as_int(self):
        filter_range = FilterRange(from_='10', to='50')

        filter_range.parse(ValueKind.Integer)

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.Integer
        assert filter_range.from_ == 10
        assert filter_range.to == 50

    def test_should_run_when_parse_as_float(self):
        filter_range = FilterRange(from_='10.5', to='50.5')

        filter_range.parse(ValueKind.Float)

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.Float
        assert filter_range.from_ == 10.5
        assert filter_range.to == 50.5

    def test_should_run_when_parse_as_date(self):
        filter_range = FilterRange(from_='2024-01-01', to='2024-01-31')

        filter_range.parse(ValueKind.Date)

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.Date
        assert filter_range.from_.isoformat() == '2024-01-01T00:00:00'
        assert filter_range.to.isoformat() == '2024-01-31T23:59:59.999999'

    def test_should_run_when_parse_wrong_date(self):
        filter_range = FilterRange(from_='invalid-date', to='2024-01-31')

        filter_range.parse(ValueKind.Date)

        assert filter_range.has_value() is True
        assert filter_range.has_from() is False
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.Date
        assert filter_range.from_ is None
        assert filter_range.to.isoformat() == '2024-01-31T23:59:59.999999'

    def test_should_modify_values(self):
        filter_range = FilterRange(from_='10', to='50')

        filter_range.modify(from_='20', to='40')

        assert filter_range.has_value() is True
        assert filter_range.has_from() is True
        assert filter_range.has_to() is True
        assert filter_range.kind == ValueKind.String
        assert filter_range.from_ == '20'
        assert filter_range.to == '40'

    def test_should_not_parse_when_has_value(self):
        filter_range = FilterRange('11', '51')
        filter_range.modify()
        filter_range.modify(from_=10, to=50)

        filter_range.parse(ValueKind.String)

        assert filter_range.from_ == 10
        assert filter_range.to == 50
