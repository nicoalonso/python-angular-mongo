from src.domain.identity.list import FieldBase, Field


class TestFieldBase:
    def test_create(self):
        field = FieldBase('name')

        assert field.name == 'name'
        assert field.alias == 'name'

    def test_mapping(self):
        field = FieldBase('name')
        field_map = Field('field_name')
        field.mapping(field_map)

        assert field.name == 'field_name'

    def test_is_(self):
        field = FieldBase('name')

        assert field.is_('name')
        assert not field.is_('other_name')
