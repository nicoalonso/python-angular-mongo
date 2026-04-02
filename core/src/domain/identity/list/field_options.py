from .field_option import FieldOption


class FieldOptions:
    """
    A field options represents the options for a field in a list. It has three options:

    Attributes:
        can_select (bool): Whether the field can be selected.
        can_filter (bool): Whether the field can be filtered.
        can_sort (bool): Whether the field can be sorted.
    """
    def __init__(self):
        self.can_select = True
        self.can_filter = True
        self.can_sort = True

    def add_options(self, options: list[FieldOption]) -> None:
        """
        Add options to the field options.
        :param options: (list[FieldOption]) The options to add.
        """
        for option in options:
            self.add(option)

    def add(self, option: FieldOption) -> None:
        """
        Add an option to the field options.
        :param option: (FieldOption) The option to add.
        """
        match option:
            case FieldOption.NoSelect:
                self.can_select = False
            case FieldOption.NoFilter:
                self.can_filter = False
            case FieldOption.NoSort:
                self.can_sort = False
