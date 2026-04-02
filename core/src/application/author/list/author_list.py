from src.domain.author import AuthorRepository, Author
from src.domain.identity.list import Field, FieldMapRecord
from src.application.identity.list import EntityList


class AuthorList(EntityList[Author]):
    """
    Author list use case
    """
    author_mapping: FieldMapRecord = [
        Field('name'),
        Field('realName'),
        Field('nationality'),
    ]

    def __init__(self, repository: AuthorRepository):
        super().__init__(repository, self.author_mapping)
