from src.domain.identity.list import SortField, Field
from src.domain.identity.list.sort_field import SortDirection


class TestSortField:
    def test_should_create(self):
        sort_field = SortField('number')

        assert sort_field.name == 'number'
        assert sort_field.alias == 'number'
        assert sort_field.direction == SortDirection.Ascending
        assert sort_field.is_ascending() is True
        assert sort_field.is_descending() is False

    def test_should_valid_when_create_from_string_without_direction(self):
        sort_field = SortField.from_string('number')

        assert sort_field.name == 'number'
        assert sort_field.alias == 'number'
        assert sort_field.direction == SortDirection.Ascending
        assert sort_field.is_ascending() is True
        assert sort_field.is_descending() is False

    def test_should_asc_when_create_from_string_with_asc_direction(self):
        sort_field = SortField.from_string('+number')

        assert sort_field.name == 'number'
        assert sort_field.alias == 'number'
        assert sort_field.direction == SortDirection.Ascending
        assert sort_field.is_ascending() is True
        assert sort_field.is_descending() is False

    def test_should_desc_when_create_from_string_with_desc_direction(self):
        sort_field = SortField.from_string('-number')

        assert sort_field.name == 'number'
        assert sort_field.alias == 'number'
        assert sort_field.direction == SortDirection.Descending
        assert sort_field.is_ascending() is False
        assert sort_field.is_descending() is True

    def test_should_run_when_update_by_mapping(self):
        sort_field = SortField('number')
        field = Field('number', name='invoice.number')
        sort_field.mapping(field)

        assert sort_field.alias == 'number'
        assert sort_field.name == 'invoice.number'
