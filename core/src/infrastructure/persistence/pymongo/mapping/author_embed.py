from pydantic import BaseModel


class AuthorEmbed(BaseModel):
    id: str
    name: str
