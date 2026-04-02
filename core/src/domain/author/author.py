from dataclasses import dataclass
from datetime import timedelta, datetime
from dateutil.utils import today

from src.domain.author.exception import InvalidBirthDateError, InvalidDeathDateError
from src.domain.identity import Entity
from src.domain.identity.exception import NameEmptyError
from .author_descriptor import AuthorDescriptor


@dataclass
class Author(Entity):
    """
    Author entity represents an author in the system.

    Attributes:
        name (str): The name of the author.
        real_name (str): The real name of the author.
        genres (str): The genres associated with the author.
        biography (str): A brief biography of the author
        nationality (str): The nationality of the author.
        birth_date (date): The birthdate of the author.
        death_date (date | None): The death date of the author, if applicable.
        photo_url (str): A URL to a photo of the author.
        website (str): The official website of the author.
    """
    name: str = None
    real_name: str = None
    genres: str = None
    biography: str = None
    nationality: str = None
    birth_date: datetime = None
    death_date: datetime | None = None
    photo_url: str = None
    website: str = None

    @classmethod
    def create(
            cls,
            name: str,
            real_name: str,
            genres: str,
            biography: str,
            nationality: str,
            birth_date: datetime,
            death_date: datetime | None = None,
            photo_url: str = None,
            website: str = None,
            created_by: str = None,
        ) -> "Author":
        """
        Factory method to create a new Author instance.
        """
        cls.check(name, birth_date, death_date)

        return cls(
            name=name,
            real_name=real_name,
            genres=genres,
            biography=biography,
            nationality=nationality,
            birth_date=birth_date,
            death_date=death_date,
            photo_url=photo_url,
            website=website,
            created_by=created_by
        )

    def modify(
            self,
            name: str,
            real_name: str,
            genres: str,
            biography: str,
            nationality: str,
            birth_date: datetime,
            death_date: datetime | None,
            photo_url: str,
            website: str,
            updated_by: str
    ) -> None:
        """
        Modifies the Author instance with new data.
        """
        self.check(name, birth_date, death_date)

        self.name = name
        self.real_name = real_name
        self.genres = genres
        self.biography = biography
        self.nationality = nationality
        self.birth_date = birth_date
        self.death_date = death_date
        self.photo_url = photo_url
        self.website = website
        self.updated(updated_by)

    @classmethod
    def check(cls, name: str, birth_date: datetime, death_date: datetime | None):
        """
        Validates the input data for creating an Author instance.

        :raises NameEmptyError: If the name is empty.
        :raises InvalidBirthDateError: If the birthdate is in the future.
        :raises InvalidDeathDateError: If the death date is in the future or before the birthdate.
        """
        if not name:
            raise NameEmptyError()

        today_ = today()

        if birth_date > today_:
            raise InvalidBirthDateError()

        if death_date:
            tomorrow = today_ + timedelta(days=1)
            if death_date > tomorrow:
                raise InvalidDeathDateError()
            elif death_date < birth_date:
                raise InvalidDeathDateError('Death date cannot be before birth date.')

    def get_descriptor(self) -> AuthorDescriptor:
        """
        Returns an AuthorDescriptor instance containing the data of the Author.
        """
        return AuthorDescriptor(
            id=self.id,
            name=self.name,
        )
