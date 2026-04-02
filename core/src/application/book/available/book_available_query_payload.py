from pydantic import BaseModel, Field


class BookAvailableQueryPayload(BaseModel):
    """Book available list filters"""
    is_sale: bool = Field(default=False, alias='sale', examples=[True, False])
