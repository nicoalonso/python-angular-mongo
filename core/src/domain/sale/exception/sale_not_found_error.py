from src.domain.identity.exception import NotFoundError


class SaleNotFoundError(NotFoundError):
    def __init__(self, sale_id: str):
        super().__init__(f"Sale with id '{sale_id}' not found")
