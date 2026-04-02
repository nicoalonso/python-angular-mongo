from pydantic import BaseModel, Field


class SummaryCreatePayload(BaseModel):
    """
    Payload for creating a summary.

    :ivar url: URL to summarize
    :ivar type: Type of summary (e.g., "description", "biography")
    """
    url: str = Field(examples=['https://es.wikipedia.org/wiki/Stephen_King'])
    type: str = Field(examples=['description', 'biography'])
