from fastapi import Depends

from src.application.summary.creator import SummaryCreate
from src.application.summary.reader import SummaryRead
from src.infrastructure.dependencies.bus import get_bus
from src.infrastructure.dependencies.repository import get_summary_repository, get_user_repository


def get_summary_creator(
        repo_summary = Depends(get_summary_repository),
        repo_user = Depends(get_user_repository),
        bus = Depends(get_bus)
) -> SummaryCreate:
    return SummaryCreate(repo_summary, repo_user, bus)


def get_summary_reader(
        repo_summary = Depends(get_summary_repository),
) -> SummaryRead:
    return SummaryRead(repo_summary)



__all__ = [
    "get_summary_creator",
    "get_summary_reader",
]
