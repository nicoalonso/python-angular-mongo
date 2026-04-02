from pydantic import BaseModel, Field

from src.domain.identity.list import Pagination


class PaginationView(BaseModel):
    total: int
    page: int
    rows_per_page: int = Field(serialization_alias='rowsPerPage')
    total_pages: int = Field(serialization_alias='totalPages')

    @staticmethod
    def serialize(pagination: Pagination) -> 'PaginationView':
        """Serialize a Pagination object to a PaginationView"""
        return PaginationView(
            total=pagination.total,
            page=pagination.page,
            rows_per_page=pagination.rows_per_page,
            total_pages=pagination.total_pages
        )
