from pydantic import BaseModel

from src.presentation.identity import Result


class BookAvailableViewData(BaseModel):
    available: bool


class BookAvailableView(Result[BookAvailableViewData]):
    def __init__(self, available: bool):
        super().__init__(data=BookAvailableViewData(available=available))
