from enum import Enum


class FilterType(Enum):
    Wildcard = "ft:wildcard"
    Match = 'ft:match',
    Fuzzy = 'ft:fuzzy',
    Range = 'ft:range',
    In = 'ft:in',
    All = 'ft:all',
    Exists = 'ft:exists',

    @classmethod
    def check(cls, filter_type) -> bool:
        """
        Checks if the given filter type is a valid filter type
        :param filter_type:
        :return: boolean
        """
        return filter_type in cls

    def is_value_list(self):
        return self in [FilterType.In, FilterType.All]
