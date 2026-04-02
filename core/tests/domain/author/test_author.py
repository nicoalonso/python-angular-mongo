from datetime import timedelta, datetime

import pytest
from dateutil.utils import today

from src.domain.author import Author
from src.domain.author.exception import InvalidBirthDateError, InvalidDeathDateError
from src.domain.identity.exception import NameEmptyError


class TestAuthor:
    def test_fail_when_name_is_empty(self):
        with pytest.raises(NameEmptyError):
            Author.create(
                name='',
                real_name='William Shakespeare',
                genres='Tragedy, Comedy, History',
                biography='William Shakespeare was an English playwright, poet, and actor.',
                nationality='English',
                birth_date=datetime(1564, 4, 23),
                death_date=datetime(1616, 4, 23),
                photo_url='https://example.com/shakespeare.jpg',
                website='https://en.wikipedia.org/wiki/William_Shakespeare',
                created_by='test',
            )

    def test_fail_when_invalid_birth_date(self):
        birth_date = today() + timedelta(days=1)

        with pytest.raises(InvalidBirthDateError):
            Author.create(
                name='William Shakespeare',
                real_name='William Shakespeare',
                genres='Tragedy, Comedy, History',
                biography='William Shakespeare was an English playwright, poet, and actor.',
                nationality='English',
                birth_date=birth_date,
                death_date=datetime(1616, 4, 23),
                photo_url='https://example.com/shakespeare.jpg',
                website='https://en.wikipedia.org/wiki/William_Shakespeare',
                created_by='test',
            )

    def test_fail_when_invalid_death_date(self):
        death_date = today() + timedelta(days=2)

        with pytest.raises(InvalidDeathDateError):
            Author.create(
                name='William Shakespeare',
                real_name='William Shakespeare',
                genres='Tragedy, Comedy, History',
                biography='William Shakespeare was an English playwright, poet, and actor.',
                nationality='English',
                birth_date=datetime(1564, 4, 23),
                death_date=death_date,
                photo_url='https://example.com/shakespeare.jpg',
                website='https://en.wikipedia.org/wiki/William_Shakespeare',
                created_by='test',
            )

    def test_fail_when_invalid_death_date_before_birth_date(self):
        with pytest.raises(InvalidDeathDateError):
            Author.create(
                name='William Shakespeare',
                real_name='William Shakespeare',
                genres='Tragedy, Comedy, History',
                biography='William Shakespeare was an English playwright, poet, and actor.',
                nationality='English',
                birth_date=datetime(1616, 4, 23),
                death_date=datetime(1564, 4, 23),
                photo_url='https://example.com/shakespeare.jpg',
                website='https://en.wikipedia.org/wiki/William_Shakespeare',
                created_by='test',
            )

    def test_create_author(self):
        author = Author.create(
            name='William Shakespeare',
            real_name='William Shakespeare',
            genres='Tragedy, Comedy, History',
            biography='William Shakespeare was an English playwright, poet, and actor.',
            nationality='English',
            birth_date=datetime(1564, 4, 23),
            death_date=datetime(1616, 4, 23),
            photo_url='https://example.com/shakespeare.jpg',
            website='https://en.wikipedia.org/wiki/William_Shakespeare',
            created_by='test',
        )

        assert author.id is not None
        assert author.name == 'William Shakespeare'
        assert author.real_name == 'William Shakespeare'
        assert author.genres == 'Tragedy, Comedy, History'
        assert author.biography == 'William Shakespeare was an English playwright, poet, and actor.'
        assert author.nationality == 'English'
        assert author.birth_date == datetime(1564, 4, 23)
        assert author.death_date == datetime(1616, 4, 23)
        assert author.photo_url == 'https://example.com/shakespeare.jpg'
        assert author.website == 'https://en.wikipedia.org/wiki/William_Shakespeare'
        assert author.created_by == 'test'
        assert author.created_at is not None
        assert author.updated_by is None
        assert author.updated_at is None

    def test_modify_author(self):
        author = Author.create(
            name='William Shakespeare',
            real_name='William Shakespeare',
            genres='Tragedy, Comedy, History',
            biography='William Shakespeare was an English playwright, poet, and actor.',
            nationality='English',
            birth_date=datetime(1564, 4, 23),
            death_date=datetime(1616, 4, 23),
            photo_url='https://example.com/shakespeare.jpg',
            website='https://en.wikipedia.org/wiki/William_Shakespeare',
            created_by='test',
        )

        author.modify(
            name='William Shakespeare Modified',
            real_name='William Shakespeare Modified',
            genres='Tragedy, Comedy, History',
            biography='William Shakespeare was an English playwright, poet, and actor.',
            nationality='English',
            birth_date=datetime(1564, 4, 23),
            death_date=None,
            photo_url='https://example.com/shakespeare.jpg',
            website='https://en.wikipedia.org/wiki/William_Shakespeare',
            updated_by='me',
        )

        assert author.name == 'William Shakespeare Modified'
        assert author.real_name == 'William Shakespeare Modified'
        assert author.death_date is None

    def test_should_run_get_descriptor(self):
        author = Author.create(
            name='William Shakespeare',
            real_name='William Shakespeare',
            genres='Tragedy, Comedy, History',
            biography='William Shakespeare was an English playwright, poet, and actor.',
            nationality='English',
            birth_date=datetime(1564, 4, 23),
            death_date=datetime(1616, 4, 23),
            photo_url='https://example.com/shakespeare.jpg',
            website='https://en.wikipedia.org/wiki/William_Shakespeare',
            created_by='test',
        )

        descriptor = author.get_descriptor()

        assert descriptor.id == author.id
        assert descriptor.name == author.name
