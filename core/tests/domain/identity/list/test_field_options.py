from src.domain.identity.list import FieldOptions, FieldOption


class TestFieldOptions:
    def test_should_create(self):
        options = FieldOptions()

        assert options.can_select is True
        assert options.can_filter is True
        assert options.can_sort is True

    def test_should_add_option(self):
        options = FieldOptions()
        options.add(FieldOption.NoSelect)
        options.add(FieldOption.NoFilter)
        options.add(FieldOption.NoSort)

        assert options.can_select is False
        assert options.can_filter is False
        assert options.can_sort is False

    def test_should_add_options(self):
        options = FieldOptions()
        options.add_options([
            FieldOption.NoFilter,
            FieldOption.NoSort,
        ])

        assert options.can_select is True
        assert options.can_filter is False
        assert options.can_sort is False
