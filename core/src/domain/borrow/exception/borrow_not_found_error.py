from src.domain.identity.exception import NotFoundError


class BorrowNotFoundError(NotFoundError):
    def __init__(self, borrow_id: str):
        self.borrow_id = borrow_id
        super().__init__(f"Borrow with ID {borrow_id} not found.")
