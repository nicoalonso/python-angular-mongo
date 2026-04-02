from src.domain.identity.exception import NotFoundError


class EditorialNotFoundError(NotFoundError):
    def __init__(self, editorial_id: str):
        self.editorial_id = editorial_id
        super().__init__(f"Editorial with ID {editorial_id} not found.")
