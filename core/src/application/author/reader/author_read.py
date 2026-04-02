from src.domain.author import AuthorRepository, Author
from src.domain.author.exception import AuthorNotFoundError


class AuthorRead:
    """
    Use case for reading authors.
    """
    def __init__(self, repo_author: AuthorRepository):
        self.repo_author = repo_author

    async def dispatch(self, author_id: str) -> Author:
        author = await self.repo_author.obtain_by_id(author_id)
        if not author:
            raise AuthorNotFoundError(author_id)

        return author
