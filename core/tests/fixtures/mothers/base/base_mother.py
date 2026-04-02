from abc import ABC
from typing import Any, Callable, Optional

from dateutil.parser import parse

from .mother_mapping import MotherMapping


class BaseMother(ABC):
    @classmethod
    def _merge(cls, base: dict, overrides: dict) -> dict:
        """Merges the base dictionary with the overrides."""
        values = base.copy()

        for key, value in values.items():
            if key in overrides and overrides[key] is not None:
                values[key] = overrides[key]
                continue

            (value, mapping, builder) = cls._get_mapping(value)
            values[key] = cls._apply_mapping(value, mapping, builder)

        return values

    @staticmethod
    def _get_mapping(item: Any) -> tuple[Any, MotherMapping, Optional[Callable]]:
        """Returns the value, mapping, and builder for the given value."""
        if not isinstance(item, list):
            if callable(item):
                return None, MotherMapping.MOTHER, item
            return item, MotherMapping.NONE, None

        value = None
        mapping = MotherMapping.NONE
        builder = None

        for element in item:
            if isinstance(element, MotherMapping):
                mapping = element
            elif callable(element):
                builder = element
            else:
                value = element

        if builder is not None:
            mapping = MotherMapping.MOTHER
            value = None

        return value, mapping, builder

    @staticmethod
    def _apply_mapping(value: Any, mapping: MotherMapping, builder: Optional[Callable]) -> Any:
        """Applies the mapping to the value using the builder."""
        if mapping == MotherMapping.REQUIRED and value is None:
            raise ValueError("Value is required but not provided.")

        if mapping == MotherMapping.MOTHER and builder is not None and value is None:
            return builder()

        if mapping == MotherMapping.DATE and isinstance(value, str):
            return parse(value)

        return value
