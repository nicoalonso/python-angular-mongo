from src.domain.identity.exception import BadRequestError


class AuthorBookAssociatedError(BadRequestError):
    """Raised when trying to delete an author that is associated with a book."""
    def __init__(self, author_id: str):
        super().__init__(f"Author with ID '{author_id}' is associated with a book and cannot be deleted.")
