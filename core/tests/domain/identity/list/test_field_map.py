from src.domain.identity.list import FieldBase, Field, FieldOption, FilterField, FilterType, ValueKind, FilterRange
from src.domain.identity.list.field_map import FieldMap


class TestFieldMap:
    def test_create_as_empty(self):
        field_mapping = FieldMap([])

        filter_ = FieldBase('any')

        assert field_mapping.fields.is_empty()
        assert field_mapping.has_field('any') is False
        assert field_mapping.can_select(filter_) is False
        assert field_mapping.can_filter(filter_) is False
        assert field_mapping.can_sort(filter_) is False

    def test_cannot_select_when_alias_not_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FieldBase('test')

        assert field_mapping.can_select(filter_) is False

    def test_cannot_select_when_alias_found_and_disable_select(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number', options=[FieldOption.NoSelect]),
        ])

        filter_ = FieldBase('number')

        assert field_mapping.can_select(filter_) is False

    def test_can_select_and_update_field_when_alias_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FieldBase('number')

        assert field_mapping.can_select(filter_) is True
        assert filter_.alias == 'number'
        assert filter_.name == 'invoice.number'

    def test_cannot_filter_when_alias_not_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FilterField('test', 'value1')

        assert field_mapping.can_filter(filter_) is False

    def test_cannot_filter_when_alias_found_and_disable_select(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number', options=[FieldOption.NoFilter]),
        ])

        filter_ = FilterField('number', 'value1')

        assert field_mapping.can_filter(filter_) is False

    def test_can_filter_and_update_field_when_alias_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FilterField('number', 'value1')

        assert field_mapping.can_filter(filter_) is True
        assert filter_.alias == 'number'
        assert filter_.name == 'invoice.number'

    def test_can_filter_and_update_field_type_when_alias_found(self):
        field_mapping = FieldMap([
            Field('date', name='createdAt', type_=FilterType.Range, kind=ValueKind.Date),
        ])

        filter_ = FilterField('date', '2025-01-01')

        assert field_mapping.can_filter(filter_) is True
        assert filter_.alias == 'date'
        assert filter_.name == 'createdAt'
        assert filter_.type_ == FilterType.Range
        assert filter_.kind == ValueKind.Date
        assert isinstance(filter_.value, FilterRange)

    def test_cannot_sort_when_alias_not_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FieldBase('test')

        assert field_mapping.can_sort(filter_) is False

    def test_cannot_short_when_alias_found_and_disable_sort(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number', options=[FieldOption.NoSort]),
        ])

        filter_ = FieldBase('number')

        assert field_mapping.can_sort(filter_) is False

    def test_should_can_sort_and_update_field_when_alias_found(self):
        field_mapping = FieldMap([
            Field('number', name='invoice.number'),
        ])

        filter_ = FieldBase('number')

        assert field_mapping.can_sort(filter_) is True
        assert filter_.alias == 'number'
        assert filter_.name == 'invoice.number'
