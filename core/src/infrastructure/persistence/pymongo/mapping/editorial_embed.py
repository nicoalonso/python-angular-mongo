from pydantic import BaseModel


class EditorialEmbed(BaseModel):
    id: str
    name: str
