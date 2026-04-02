from datetime import datetime

from src.domain.identity.list import FilterField, FilterType, ValueKind, FilterRangeInterval, FilterRange, Field


class TestFilterField:
    def test_should_create(self):
        filter_field = FilterField('test', 'value1')

        assert filter_field.alias == 'test'
        assert filter_field.name == 'test'
        assert filter_field.raw == 'value1'
        assert filter_field.value == 'value1'
        assert filter_field.has_value()
        assert filter_field.type_ == FilterType.Wildcard
        assert filter_field.kind == ValueKind.String
        assert filter_field.is_range() == False
        assert filter_field.is_list() == False

    def test_should_has_not_value_when_is_empty(self):
        filter_field = FilterField('test', '')

        assert filter_field.has_value() is False

    def test_should_has_not_value_when_is_none(self):
        filter_field = FilterField('test', '')
        filter_field.change_value(None)

        assert filter_field.has_value() is False

    def test_should_value_when_create(self):
        filter_field = FilterField(
            'test',
            'value1',
            type_=FilterType.Match,
            kind=ValueKind.Boolean,
            value=True,
        )

        assert filter_field.raw == 'value1'
        assert filter_field.value is True
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Boolean

    def test_should_change_value(self):
        filter_field = FilterField('test', 'value1')

        filter_field.change_value('value2', FilterType.Fuzzy, ValueKind.Integer)

        assert filter_field.raw == 'value1'
        assert filter_field.value == 'value2'
        assert filter_field.has_value()
        assert filter_field.type_ == FilterType.Fuzzy
        assert filter_field.kind == ValueKind.Integer

    def test_should_none_when_interval_is_none(self):
        filter_field = FilterField('test', '1234')
        filter_field.range(FilterRangeInterval.Empty, '5678')

        assert not isinstance(filter_field, FilterRange)
        assert filter_field.value == '1234'

    def test_make_when_range_to(self):
        filter_field = FilterField('test', '1234', type_=FilterType.Range)
        filter_field.range(FilterRangeInterval.To, '5678')

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.is_range()
        assert filter_field.has_value()
        assert filter_field.value.has_from() == False
        assert filter_field.value.has_to() == True
        assert filter_field.value.to == '5678'

    def test_make_when_range_empty_to(self):
        filter_field = FilterField('test', '', type_=FilterType.Range)
        filter_field.range(FilterRangeInterval.To, '')

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.is_range()
        assert filter_field.has_value() == False
        assert filter_field.value.has_value() == False

    def test_make_when_range_from(self):
        filter_field = FilterField('test', '1234', type_=FilterType.Range)
        filter_field.range(FilterRangeInterval.From, '5678')

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.is_range()
        assert filter_field.has_value()
        assert filter_field.value.has_from() == True
        assert filter_field.value.has_to() == False
        assert filter_field.value.from_ == '5678'

    def test_update_when_range_to(self):
        filter_range = FilterRange(from_='1234')
        filter_field = FilterField('test', '1234', type_=FilterType.Range, value=filter_range)
        filter_field.range(FilterRangeInterval.To, '5678')

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.is_range()
        assert filter_field.has_value()
        assert filter_field.value.has_from() == True
        assert filter_field.value.has_to() == True
        assert filter_field.value.from_ == '1234'
        assert filter_field.value.to == '5678'

    def test_update_when_range_from(self):
        filter_range = FilterRange(to='1234')
        filter_field = FilterField('test', '1234', type_=FilterType.Range, value=filter_range)
        filter_field.range(FilterRangeInterval.From, '5678')

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.is_range()
        assert filter_field.has_value()
        assert filter_field.value.has_from() == True
        assert filter_field.value.has_to() == True
        assert filter_field.value.from_ == '5678'
        assert filter_field.value.to == '1234'

    def test_should_run_when_mapped_as_boolean(self):
        field = Field('dummy', type_=FilterType.Match, kind=ValueKind.Boolean)
        filter_field = FilterField('test', 'TRUE')

        filter_field.mapping(field)

        assert filter_field.value == True
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Boolean
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_boolean_as_false(self):
        field = Field('dummy', type_=FilterType.Match, kind=ValueKind.Boolean)
        filter_field = FilterField('test', 'FALSE')

        filter_field.mapping(field)

        assert filter_field.value == False
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Boolean
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_boolean_as_wrong_string(self):
        field = Field('dummy', type_=FilterType.Match, kind=ValueKind.Boolean)
        filter_field = FilterField('test', "wrong")

        filter_field.mapping(field)

        assert filter_field.value == False
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Boolean
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_integer(self):
        field = Field('dummy', type_=FilterType.Match, kind=ValueKind.Integer)
        filter_field = FilterField('test', '1234')

        filter_field.mapping(field)

        assert filter_field.value == 1234
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Integer
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_zero_integer(self):
        field = Field('dummy', type_=FilterType.Match, kind=ValueKind.Integer)
        filter_field = FilterField('test', '0')

        filter_field.mapping(field)

        assert filter_field.value == 0
        assert filter_field.type_ == FilterType.Match
        assert filter_field.kind == ValueKind.Integer
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_zero_date(self):
        field = Field('dummy', kind=ValueKind.Date)
        filter_field = FilterField('test', '2025-01-01')

        filter_field.mapping(field)

        assert isinstance(filter_field.value, datetime)
        assert filter_field.type_ == FilterType.Wildcard
        assert filter_field.kind == ValueKind.Date
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_range_date(self):
        field = Field('dummy', type_=FilterType.Range, kind=ValueKind.Date)
        filter_field = FilterField('test', '2025-01-01')

        filter_field.mapping(field)

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.type_ == FilterType.Range
        assert filter_field.kind == ValueKind.Date
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_date_and_has_range(self):
        filter_field = FilterField('test', '2025-01-01', type_=FilterType.Range)
        filter_field.range(FilterRangeInterval.From, '2025-01-01')
        filter_field.range(FilterRangeInterval.To, '2025-12-31')

        field = Field('dummy', type_=FilterType.Range, kind=ValueKind.Date)
        filter_field.mapping(field)

        assert isinstance(filter_field.value, FilterRange)
        assert filter_field.type_ == FilterType.Range
        assert filter_field.kind == ValueKind.Date
        assert filter_field.has_value()
        assert filter_field.value.has_from() == True
        assert filter_field.value.has_to() == True
        assert filter_field.value.from_ == datetime(2025, 1, 1)
        assert filter_field.value.to == datetime(2025, 12, 31, 23, 59, 59, 999999)

    def test_should_run_when_mapped_as_list(self):
        field = Field('dummy', type_=FilterType.In)
        filter_field = FilterField('test', 'value1,value2,value3')

        filter_field.mapping(field)

        assert filter_field.value == ['value1', 'value2', 'value3']
        assert filter_field.type_ == FilterType.In
        assert filter_field.kind == ValueKind.String
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_integer_list(self):
        field = Field('dummy', type_=FilterType.In, kind=ValueKind.Integer)
        filter_field = FilterField('test', '1,2,3')

        filter_field.mapping(field)

        assert filter_field.value == [1, 2, 3]
        assert filter_field.type_ == FilterType.In
        assert filter_field.kind == ValueKind.Integer
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_float_list(self):
        field = Field('dummy', type_=FilterType.In, kind=ValueKind.Float)
        filter_field = FilterField('test', '1,2,3')

        filter_field.mapping(field)

        assert filter_field.value == [1, 2, 3]
        assert filter_field.type_ == FilterType.In
        assert filter_field.kind == ValueKind.Float
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_bool_list(self):
        field = Field('dummy', type_=FilterType.In, kind=ValueKind.Boolean)
        filter_field = FilterField('test', '1,2,3')

        filter_field.mapping(field)

        assert filter_field.value == [True, False, False]
        assert filter_field.type_ == FilterType.In
        assert filter_field.kind == ValueKind.Boolean
        assert filter_field.has_value()

    def test_should_run_when_mapped_as_date_list(self):
        field = Field('dummy', type_=FilterType.In, kind=ValueKind.Date)
        filter_field = FilterField('test', '2024-01-01,2025-01-01,invalid')

        filter_field.mapping(field)

        assert len(filter_field.value) == 2
        assert isinstance(filter_field.value[0], datetime)
        assert isinstance(filter_field.value[1], datetime)
        assert filter_field.type_ == FilterType.In
        assert filter_field.kind == ValueKind.Date
        assert filter_field.has_value()
