from datetime import datetime
from typing import Optional

from .filter_type import FilterType
from .value_kind import ValueKind
from .filter_range_interval import FilterRangeInterval
from .filter_range import FilterRange
from .field import Field
from .field_base import FieldBase
from .. import Collection

type FilterValueType = str | bool | int | float | datetime | list[str] | list[int] | list[float] | list[datetime] | FilterRange | None


class FilterField(FieldBase):
    """
    A filter field represents a field that can be used for filtering in a list.

    :ivar raw: (str) The raw value of the filter field, as provided in the query.
    :ivar type_: (FilterType) The filter type for the field, which determines how the filter should be applied.
    :ivar kind: (ValueKind) The value kind for the field which determines the type of the value for the filter.
    :ivar value: (FilterValueType) The value of the filter field, which is the processed value that will be used for filtering in the list.
    """
    def __init__(
            self,
            name: str,
            raw: str,
            *,
            type_: Optional[FilterType] = None,
            kind: Optional[ValueKind] = None,
            value: Optional[FilterValueType] = None,
    ):
        super().__init__(name)

        self.raw = raw
        self.type_ = type_ or FilterType.Wildcard
        self.kind = kind or ValueKind.String
        self.value = value or raw

    def change_value(
            self,
            new_value: FilterValueType,
            new_type: Optional[FilterType] = None,
            new_kind: Optional[ValueKind] = None,
    ) -> None:
        """
        Changes the value of the filter field and optionally updates the filter type and value kind.
        :param new_value: The new value for the filter field.
        :param new_type: The new filter type for the field, if applicable.
        :param new_kind: The new value kind for the field, if applicable.
        """
        self.value = new_value
        if new_type:
            self.type_ = new_type

        if new_kind:
            self.kind = new_kind

    def range(self, interval: FilterRangeInterval, value: str) -> None:
        """
        Modifies the value of the filter field as a range based on the provided interval and value.
        :param interval: (FilterRangeInterval) The interval to modify (From, To, or Empty).
        :param value: (str) The value to set for the specified interval.
        """
        if interval == FilterRangeInterval.Empty:
            return

        if self.is_range():
            if interval == FilterRangeInterval.From:
                self.value.modify(from_=value)
            elif interval == FilterRangeInterval.To:
                self.value.modify(to=value)
            return

        if interval == FilterRangeInterval.From:
            self.value = FilterRange(from_=value)
        elif interval == FilterRangeInterval.To:
            self.value = FilterRange(to=value)

    def mapping(self, field: Field):
        """Map the field base to a field

        :param field: (Field) The field to map to
        """
        super().mapping(field)
        self.type_ = field.type_
        self.kind = field.kind
        self._parse_value()

    def _parse_value(self) -> None:
        """Parse the raw value of the filter field based on its filter type and value kind, and update the value accordingly."""
        if self.type_.is_value_list():
            self._parse_list()
            return

        if self.type_ == FilterType.Range:
            self._parse_range()
            return

        self.value = self.kind.parse(self.raw)

    def _parse_range(self) -> None:
        """Parse the raw value of the filter field as a range, and update the value accordingly."""
        if not self.is_range():
            self.value = FilterRange(from_=self.raw,)

        self.value.parse(self.kind)

    def _parse_list(self) -> None:
        """Parse the raw value of the filter field as a list, and update the value accordingly."""
        list_values = self.kind.to_list(self.raw)

        match self.kind:
            case ValueKind.Integer:
                self.value = [self.kind.to_int(value) for value in list_values]
            case ValueKind.Float:
                self.value = [self.kind.to_float(value) for value in list_values]
            case ValueKind.Boolean:
                self.value = [self.kind.to_bool(value) for value in list_values]
            case ValueKind.Date:
                self.value = list(
                    filter(
                        lambda value: value is not None,
                        map(lambda value: self.kind.to_date(value), list_values)
                    )
                )
            case _:
                self.value = list_values

    def has_value(self) -> bool:
        """Check if the filter field has a value that can be used for filtering"""
        if self.value is None:
            return False

        if self.is_range():
            return self.value.has_value()

        return (
            isinstance(self.value, (bool, int, float, datetime))
            or (isinstance(self.value, str) and len(self.value) > 0)
            or (isinstance(self.value, list) and len(self.value) > 0)
        )

    def is_range(self) -> bool:
        """Check if the value of the filter field is a range"""
        return isinstance(self.value, FilterRange)

    def is_list(self) -> bool:
        """Check if the value of the filter field is a list"""
        return isinstance(self.value, list)


type FilterFieldCollection = Collection[FilterField]
