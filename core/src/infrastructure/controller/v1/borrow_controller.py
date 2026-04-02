from typing import Annotated

from fastapi import Query, Depends, HTTPException

from src.application.borrow.sanctioner.borrow_penalty_event import BorrowPenaltyEvent
from src.domain.borrow.exception import BorrowNotFoundError
from src.domain.bus import DomainBus
from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.borrow.checkin import BorrowCheckinPayload, BorrowCheckin
from src.application.borrow.creator import BorrowCreatePayload, BorrowCreate
from src.application.borrow.list import BorrowQueryPayload, BorrowList
from src.application.borrow.reader import BorrowRead
from src.infrastructure.dependencies.borrow import *
from src.infrastructure.dependencies.bus import get_bus
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.borrow import BorrowListViewData, BorrowReadView, BorrowListView


@router.get("/borrows", tags=["Borrows"], summary='Get all borrows')
async def get_borrows(
        query_params: Annotated[BorrowQueryPayload, Query()],
        lister: Annotated[BorrowList, Depends(get_borrow_list)]
) -> ListView[BorrowListViewData]:
    """Get all borrows with pagination and filters."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, BorrowListViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/borrows", tags=["Borrows"], status_code=201, summary='Create a new borrow')
async def create_borrow(
        payload: BorrowCreatePayload,
        creator: Annotated[BorrowCreate, Depends(get_borrow_creator)],
) -> BorrowListView:
    """Create a new borrow with customer and book details"""
    try:
        borrow = await creator.dispatch(payload)
        return BorrowListView(borrow)
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/borrows/{borrow_id}", tags=["Borrows"], summary='Get borrow by id')
async def get_borrow(
        borrow_id: str,
        reader: Annotated[BorrowRead, Depends(get_borrow_reader)]
) -> BorrowReadView:
    """Get a borrow by its ID, including customer and book details."""
    try:
        borrow = await reader.dispatch(borrow_id)
        return BorrowReadView(borrow)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/borrows/{borrow_id}", tags=["Borrows"], status_code=204, summary='Checkin a borrow')
async def checkin_borrow(
        borrow_id: str,
        payload: BorrowCheckinPayload,
        updater: Annotated[BorrowCheckin, Depends(get_borrow_checker)],
) -> None:
    """Checkin a borrow by its ID, updating the return date."""
    try:
        await updater.dispatch(borrow_id, payload)
    except BorrowNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (BadRequestError, NotFoundError) as e:  # pragma: no cover
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/borrows/manual-penalty", tags=["Borrows"], status_code=202, summary='Manual penalty')
async def manual_penalty(bus: Annotated[DomainBus, Depends(get_bus)]) -> None:
    """Execute manual penalty calculation for overdue borrows."""
    try:
        event = BorrowPenaltyEvent()
        await bus.dispatch(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "get_borrows",
    "create_borrow",
    "get_borrow",
    "checkin_borrow",
    "manual_penalty",
]
