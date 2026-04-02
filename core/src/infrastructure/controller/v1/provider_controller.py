from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Query, Depends

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.provider.creator import ProviderCreatePayload, ProviderCreate
from src.application.provider.eraser import ProviderAssociatedError, ProviderDelete
from src.application.provider.reader import ProviderRead
from src.application.provider.updater import ProviderUpdatePayload, ProviderUpdate
from src.application.provider.list import ProviderQueryPayload, ProviderList
from src.infrastructure.dependencies.provider import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.provider import ProviderReadView, ProviderReadViewData


@router.get("/providers", tags=["Providers"], summary='List all providers')
async def get_providers(
        query_params: Annotated[ProviderQueryPayload, Query()],
        lister: Annotated[ProviderList, Depends(get_provider_list)]
) -> ListView[ProviderReadViewData]:
    """List all providers with optional filtering and pagination."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, ProviderReadViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/providers", tags=["Providers"], status_code=201, summary='Create a new provider')
async def create_provider(
        payload: ProviderCreatePayload,
        creator: Annotated[ProviderCreate, Depends(get_provider_creator)],
) -> ProviderReadView:
    """Create a new provider with the given details."""
    try:
        provider = await creator.dispatch(payload)
        return ProviderReadView(provider)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers/{provider_id}", tags=["Providers"], summary='Get provider details')
async def get_provider(
        provider_id: str,
        reader: Annotated[ProviderRead, Depends(get_provider_reader)]
) -> ProviderReadView:
    """Get details of a specific provider by its ID."""
    try:
        provider = await reader.dispatch(provider_id)
        return ProviderReadView(provider)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/providers/{provider_id}", tags=["Providers"], status_code=204, summary='Update provider details')
async def update_provider(
        provider_id: str,
        payload: ProviderUpdatePayload,
        updater: Annotated[ProviderUpdate, Depends(get_provider_updater)],
) -> None:
    """Update details of a specific provider by its ID."""
    try:
        await updater.dispatch(provider_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/providers/{provider_id}", tags=["Providers"], status_code=204, summary='Delete a provider')
async def delete_provider(
        provider_id: str,
        eraser: Annotated[ProviderDelete, Depends(get_provider_eraser)]
) -> None:
    """Delete a specific provider by its ID."""
    try:
        await eraser.dispatch(provider_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProviderAssociatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "get_providers",
    "create_provider",
    "get_provider",
    "update_provider",
    "delete_provider",
]
