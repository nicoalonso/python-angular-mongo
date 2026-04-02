from pydantic import BaseModel


class ProviderEmbed(BaseModel):
    id: str
    name: str
