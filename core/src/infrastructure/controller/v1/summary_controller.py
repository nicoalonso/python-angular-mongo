from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.application.summary.creator import SummaryCreatePayload, SummaryCreate
from src.application.summary.reader import SummaryRead
from src.infrastructure.dependencies.summary import *
from src.infrastructure.router import router
from src.presentation.v1.summary import SummaryReadView


@router.post("/summaries", tags=["Summaries"], status_code=201, summary='Create a new summary')
async def create_summary(
        payload: SummaryCreatePayload,
        creator: Annotated[SummaryCreate, Depends(get_summary_creator)]
) -> SummaryReadView:
    """Create a new summary based on the provided payload."""
    try:
        summary = await creator.dispatch(payload)
        return SummaryReadView(summary)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summaries/{summary_id}", tags=["Summaries"], summary='Get a summary by ID')
async def get_summary(
        summary_id: str,
        reader: Annotated[SummaryRead, Depends(get_summary_reader)]
) -> SummaryReadView:
    """Retrieve a summary by its ID."""
    try:
        summary = await reader.dispatch(summary_id)
        return SummaryReadView(summary)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "create_summary",
    "get_summary",
]
