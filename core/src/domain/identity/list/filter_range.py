from .value_kind import ValueKind, ValueType


class FilterRange:
    """
    Filter range for list filters

    :ivar from_: (ValueType) The start value of the range
    :ivar to: (ValueType) The end value of the range
    :ivar kind: (ValueKind) The value kind of the range values
    """
    def __init__(self, from_: str = '', to: str = ''):
        self.from_: ValueType = from_
        self.to: ValueType = to
        self.kind = ValueKind.String

    def parse(self, kind: ValueKind) -> None:
        """
        Parses the from and to values to the specified value kind

        :param kind: The value kind to parse the values to
        """
        if not isinstance(self.from_, str) and not isinstance(self.to, str):
            return

        self.kind = kind
        from_value: str = self.from_
        to_value: str = self.to

        if kind == ValueKind.Date:
            from_value = from_value.strip()
            to_value = to_value.strip()

        self.from_ = kind.parse(from_value)
        self.to = kind.parse(to_value)

        if kind == ValueKind.Date and self.to is not None and kind.is_short_date(to_value):
            self.to = self.to.replace(hour=23, minute=59, second=59, microsecond=999999)

    def modify(self, from_: ValueType = None, to: ValueType = None) -> None:
        """
        Modifies the from and to values of the range

        :param from_: The new start value of the range
        :param to: The new end value of the range
        """
        if from_ is not None:
            self.from_ = from_
        if to is not None:
            self.to = to

    def has_value(self) -> bool:
        """
        Checks if the range has a from or to value

        :return: True if the range has a from or to value, False otherwise
        """
        return self.has_from() or self.has_to()

    def has_from(self) -> bool:
        """
        Checks if the range has the `from` value

        :return: True if the range has the `from` value, False otherwise
        """
        return self.from_ is not None and self.from_ != ''

    def has_to(self) -> bool:
        """
        Checks if the range has the `to` value

        :return: True if the range has the `to` value, False otherwise
        """
        return self.to is not None and self.to != ''
