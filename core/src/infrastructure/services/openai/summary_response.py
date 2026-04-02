from pydantic import BaseModel


class SummaryResponse(BaseModel):
    """
    Summary Response
    """
    summary: str
