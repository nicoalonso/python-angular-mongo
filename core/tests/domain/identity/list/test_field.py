from src.domain.identity.list import Field, FilterType, ValueKind, FieldOption


class TestField:
    def test_create(self):
        field = Field('alias')

        assert field.alias == "alias"
        assert field.field_name == "alias"
        assert field.type_ == FilterType.Wildcard
        assert field.kind == ValueKind.String
        assert field.options.can_select
        assert field.options.can_filter
        assert field.options.can_sort

    def test_define_field_name(self):
        field = Field('alias', name='field_name')

        assert field.alias == "alias"
        assert field.field_name == "field_name"

    def test_define_type_and_kind(self):
        field = Field('alias', type_=FilterType.Match, kind=ValueKind.Integer)

        assert field.type_ == FilterType.Match
        assert field.kind == ValueKind.Integer

    def test_define_options(self):
        options = [FieldOption.NoSelect, FieldOption.NoFilter, FieldOption.NoSort]
        field = Field('alias', options=options)

        assert not field.options.can_select
        assert not field.options.can_filter
        assert not field.options.can_sort
