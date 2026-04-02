from src.domain.editorial import EditorialRepository, Editorial
from src.domain.editorial.exception import EditorialNotFoundError


class EditorialRead:
    """
    Use case for reading editorials.
    """
    def __init__(self, repo_editorial: EditorialRepository):
        self.repo_editorial = repo_editorial

    async def dispatch(self, editorial_id: str) -> Editorial:
        """
        Dispatch the use case to read an editorial by its ID.
        :param editorial_id: The ID of the editorial to read.
        :return: The editorial data.
        """
        editorial = await self.repo_editorial.obtain_by_id(editorial_id)
        if not editorial:
            raise EditorialNotFoundError(editorial_id)

        return editorial
