from src.domain.identity.exception import NotFoundError


class CustomerNotFoundError(NotFoundError):
    """
    Exception raised when a customer is not found in the repository.
    """
    def __init__(self, customer_id: str):
        super().__init__(f"Customer with ID '{customer_id}' not found.")
