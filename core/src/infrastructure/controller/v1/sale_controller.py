from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Query, Depends

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.sale.creator import SaleCreatePayload, SaleCreate
from src.application.sale.list import SaleList, SaleQueryPayload
from src.application.sale.reader import SaleRead
from src.infrastructure.dependencies.sale import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.sale import SaleListViewData, SaleReadView, SaleListView


@router.get("/sales", tags=["Sales"], summary='List all sales')
async def get_sales(
        query_params: Annotated[SaleQueryPayload, Query()],
        lister: Annotated[SaleList, Depends(get_sale_list)]
) -> ListView[SaleListViewData]:
    """List all sales with optional filtering and pagination."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, SaleListViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sales", tags=["Sales"], status_code=201, summary='Create a new sale')
async def create_sale(
        payload: SaleCreatePayload,
        creator: Annotated[SaleCreate, Depends(get_sale_creator)],
) -> SaleListView:
    """Create a new sale with the provided details."""
    try:
        sale = await creator.dispatch(payload)
        return SaleListView(sale)
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales/{sale_id}", tags=["Sales"], summary='Get sale by ID')
async def get_sale(
        sale_id: str,
        reader: Annotated[SaleRead, Depends(get_sale_reader)]
) -> SaleReadView:
    """Retrieve a sale by its ID."""
    try:
        sale = await reader.dispatch(sale_id)
        return SaleReadView(sale)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "get_sales",
    "create_sale",
    "get_sale"
]
