from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Query, Depends

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.domain.purchase.exception import PurchaseNotFoundError
from src.application.purchase.creator import PurchaseCreate, PurchaseCreatePayload
from src.application.purchase.eraser import PurchaseDelete
from src.application.purchase.list import PurchaseQueryPayload, PurchaseList
from src.application.purchase.reader import PurchaseRead
from src.application.purchase.updater import PurchaseUpdatePayload, PurchaseUpdate
from src.infrastructure.dependencies.purchase import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.purchase import PurchaseListViewData, PurchaseReadView, PurchaseListView


@router.get("/purchases", tags=["Purchases"], summary='List purchases')
async def get_purchases(
        query_params: Annotated[PurchaseQueryPayload, Query()],
        lister: Annotated[PurchaseList, Depends(get_purchase_list)]
) -> ListView[PurchaseListViewData]:
    """List purchases with pagination and filtering."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, PurchaseListViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/purchases", tags=["Purchases"], status_code=201, summary='Create a new purchase')
async def create_purchase(
        payload: PurchaseCreatePayload,
        creator: Annotated[PurchaseCreate, Depends(get_purchase_creator)],
) -> PurchaseListView:
    """Create a new purchase with the provided details."""
    try:
        purchase = await creator.dispatch(payload)
        return PurchaseListView(purchase)
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/purchases/{purchase_id}", tags=["Purchases"], summary='Get purchase details')
async def get_purchase(
        purchase_id: str,
        reader: Annotated[PurchaseRead, Depends(get_purchase_reader)]
) -> PurchaseReadView:
    """Get details of a specific purchase by its ID."""
    try:
        purchase = await reader.dispatch(purchase_id)
        return PurchaseReadView(purchase)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/purchases/{purchase_id}", tags=["Purchases"], status_code=204, summary='Update purchase details')
async def update_purchase(
        purchase_id: str,
        payload: PurchaseUpdatePayload,
        updater: Annotated[PurchaseUpdate, Depends(get_purchase_updater)],
) -> None:
    """Update details of a specific purchase by its ID."""
    try:
        await updater.dispatch(purchase_id, payload)
    except PurchaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/purchases/{purchase_id}", tags=["Purchases"], status_code=204, summary='Delete a purchase')
async def delete_purchase(
        purchase_id: str,
        eraser: Annotated[PurchaseDelete, Depends(get_purchase_eraser)]
) -> None:
    """Delete a specific purchase by its ID."""
    try:
        await eraser.dispatch(purchase_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "get_purchases",
    "create_purchase",
    "get_purchase",
    "update_purchase",
    "delete_purchase",
]
