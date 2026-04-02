from pydantic import BaseModel, Field

from src.domain.sequence import SequenceNumber
from src.presentation.identity import Result


class SequenceReadViewData(BaseModel):
    number: str = Field(examples=['P-01235'])


class SequenceReadView(Result[SequenceReadViewData]):
    def __init__(self, sequence_number: SequenceNumber):
        super().__init__(data=SequenceReadViewData(number=sequence_number.format()))
