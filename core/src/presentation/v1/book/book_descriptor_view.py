from pydantic import BaseModel, Field


class BookDescriptorView(BaseModel):
    """Book descriptor read view data"""
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    title: str = Field(examples=['The Great Gatsby'])
    isbn: str = Field(examples=['978-3161484100'])
