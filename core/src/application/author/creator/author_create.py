from src.application.author.creator import AuthorCreatePayload
from src.domain.author import AuthorRepository, Author
from src.domain.author.exception import AuthorAlreadyExistsError
from src.domain.user import UserRepository


class AuthorCreate:
    """
    Use case for creating a new author.

    :ivar repo_author: Repository for author data access.
    :ivar repo_user: Repository for user data access.
    """
    def __init__(self, repo_author: AuthorRepository, repo_user: UserRepository):
        self.repo_author = repo_author
        self.repo_user = repo_user

    async def dispatch(self, payload: AuthorCreatePayload) -> Author:
        """
        Create a new author based on the provided payload.

        :param payload: Data required to create a new author.
        :return: The created Author object.
        """
        await self._check_already_exists(payload)

        user = self.repo_user.obtain_user()
        author = Author.create(
            name=payload.name,
            real_name=payload.real_name,
            genres=payload.genres,
            biography=payload.biography,
            nationality=payload.nationality,
            birth_date=payload.birth_date,
            death_date=payload.death_date,
            photo_url=payload.photo_url,
            website=payload.website,
            created_by=user.name,
        )
        await self.repo_author.save(author)

        return author

    async def _check_already_exists(self, payload: AuthorCreatePayload) -> None:
        """
        Check if an author with the same name already exists.
        :param payload: Data required to create a new author.
        """
        author = await self.repo_author.obtain_by_name(payload.name)
        if author is not None:
            raise AuthorAlreadyExistsError()
