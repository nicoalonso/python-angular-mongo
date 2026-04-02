from src.domain.identity.exception import NotFoundError


class SummaryNotFoundError(NotFoundError):
    def __init__(self, summary_id: str):
        super().__init__(f"Summary with ID {summary_id} not found.")
