from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Query, Depends

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.editorial.creator import EditorialCreatePayload, EditorialCreate
from src.application.editorial.list import EditorialQueryPayload, EditorialList
from src.application.editorial.reader import EditorialRead
from src.application.editorial.updater import EditorialUpdatePayload, EditorialUpdate
from src.application.editorial.eraser import EditorialDelete, EditorialBookAssociatedError
from src.infrastructure.dependencies.editorial import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.editorial import EditorialReadViewData, EditorialReadView


@router.get("/editorials", tags=["Editorials"], summary='Get all editorials')
async def get_editorials(
        query_params: Annotated[EditorialQueryPayload, Query()],
        lister: Annotated[EditorialList, Depends(get_editorial_list)]
) -> ListView[EditorialReadViewData]:
    """Get a list of editorials with optional filters and pagination."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, EditorialReadViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/editorials", tags=["Editorials"], status_code=201, summary='Create a new editorial')
async def create_editorial(
        payload: EditorialCreatePayload,
        creator: Annotated[EditorialCreate, Depends(get_editorial_creator)],
) -> EditorialReadView:
    """Create a new editorial with the provided data."""
    try:
        editorial = await creator.dispatch(payload)
        return EditorialReadView(editorial)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/editorials/{editorial_id}", tags=["Editorials"], summary='Get an editorial by ID')
async def get_editorial(
        editorial_id: str,
        reader: Annotated[EditorialRead, Depends(get_editorial_reader)]
) -> EditorialReadView:
    """Get the details of a specific editorial by its ID."""
    try:
        editorial = await reader.dispatch(editorial_id)
        return EditorialReadView(editorial)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editorials/{editorial_id}", tags=["Editorials"], status_code=204, summary='Update an editorial by ID')
async def update_editorial(
        editorial_id: str,
        payload: EditorialUpdatePayload,
        updater: Annotated[EditorialUpdate, Depends(get_editorial_updater)],
) -> None:
    """Update the details of a specific editorial by its ID."""
    try:
        await updater.dispatch(editorial_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/editorials/{editorial_id}", tags=["Editorials"], status_code=204, summary='Delete an editorial by ID')
async def delete_editorial(
        editorial_id: str,
        eraser: Annotated[EditorialDelete, Depends(get_editorial_eraser)]
) -> None:
    """Delete a specific editorial by its ID."""
    try:
        await eraser.dispatch(editorial_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EditorialBookAssociatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    'get_editorials',
    'create_editorial',
    'get_editorial',
    'update_editorial',
    'delete_editorial',
]
