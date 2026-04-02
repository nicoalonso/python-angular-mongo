from src.domain.author import AuthorRepository, Author
from src.domain.author.exception import AuthorNotFoundError
from src.domain.user import UserRepository
from .author_update_payload import AuthorUpdatePayload


class AuthorUpdate:
    """
    Use case for updating an author.

    :ivar repo_author: Repository for author data.
    :ivar repo_user: Repository for user data.
    """
    def __init__(self, repo_author: AuthorRepository, repo_user: UserRepository):
        self.repo_author = repo_author
        self.repo_user = repo_user

    async def dispatch(self, author_id: str, payload: AuthorUpdatePayload) -> Author:
        author = await self.repo_author.obtain_by_id(author_id)
        if not author:
            raise AuthorNotFoundError(author_id)

        user = self.repo_user.obtain_user()
        author.modify(
            name=payload.name,
            real_name=payload.real_name,
            genres=payload.genres,
            biography=payload.biography,
            nationality=payload.nationality,
            birth_date=payload.birth_date,
            death_date=payload.death_date,
            photo_url=payload.photo_url,
            website=payload.website,
            updated_by=user.name
        )

        await self.repo_author.save(author)
        return author
