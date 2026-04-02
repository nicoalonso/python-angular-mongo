from src.domain.identity.exception import NotFoundError


class AuthorNotFoundError(NotFoundError):
    def __init__(self, author_id: str):
        self.author_id = author_id
        super().__init__(f"Author with ID {author_id} not found.")
