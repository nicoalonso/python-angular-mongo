from src.domain.identity.exception import BadRequestError


class EditorialBookAssociatedError(BadRequestError):
    """Raised when a book is associated with an editorial and cannot be deleted."""
    def __init__(self, editorial_id: str):
        super().__init__(f"Cannot delete editorial {editorial_id} because it has related books.")
