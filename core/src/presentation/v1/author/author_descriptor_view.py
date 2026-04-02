from pydantic import BaseModel, Field


class AuthorDescriptorView(BaseModel):
    """Author descriptor read view data"""
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    name: str = Field(examples=['J.K. Rowling'])
