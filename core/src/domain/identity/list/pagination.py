import math


class Pagination:
    """
    Pagination class to handle pagination logic for listing items.

    :ivar total: int - Total number of items
    :ivar page: int - Current page number
    :ivar rows_per_page: int - Number of items per page
    """
    def __init__(self, total: int = 0, page: int = 1, rows_per_page: int = 10):
        self.total = total
        self.page = page
        self.rows_per_page = rows_per_page

    @property
    def total_pages(self) -> int:
        if self.total <= 0 or self.rows_per_page <= 0:
            return 0

        return math.ceil(self.total / self.rows_per_page)
