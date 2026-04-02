from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends, Query

from src.domain.identity.exception import NotFoundError, BadRequestError
from src.domain.identity.list import ListQuery
from src.application.author.creator import AuthorCreate, AuthorCreatePayload
from src.application.author.eraser import AuthorDelete, AuthorBookAssociatedError
from src.application.author.list import AuthorQueryPayload, AuthorList
from src.application.author.reader import AuthorRead
from src.application.author.updater import AuthorUpdatePayload, AuthorUpdate
from src.infrastructure.dependencies.author import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.author import AuthorReadView, AuthorReadViewData


@router.get("/authors", tags=["Authors"], summary="List Authors")
async def get_authors(
        query_params: Annotated[AuthorQueryPayload, Query()],
        lister: Annotated[AuthorList, Depends(get_author_list)]
) -> ListView[AuthorReadViewData]:
    """Get a list of authors with optional filters and pagination."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, AuthorReadViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/authors", tags=["Authors"], status_code=201, summary='Create Author')
async def create_author(
        payload: AuthorCreatePayload,
        creator: Annotated[AuthorCreate, Depends(get_author_creator)],
) -> AuthorReadView:
    """Create a new author with the provided details."""
    try:
        author = await creator.dispatch(payload)
        return AuthorReadView(author)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/authors/{author_id}", tags=["Authors"], summary='Get Author')
async def get_author(
        author_id: str,
        reader: Annotated[AuthorRead, Depends(get_author_reader)]
) -> AuthorReadView:
    """Retrieve details of a specific author by their ID."""
    try:
        author = await reader.dispatch(author_id)
        return AuthorReadView(author)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/authors/{author_id}", tags=["Authors"], status_code=204, summary='Update Author')
async def update_author(
        author_id: str,
        payload: AuthorUpdatePayload,
        updater: Annotated[AuthorUpdate, Depends(get_author_updater)],
) -> None:
    """Update an existing author's details by their ID."""
    try:
        await updater.dispatch(author_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/authors/{author_id}", tags=["Authors"], status_code=204, summary='Delete Author')
async def delete_author(
        author_id: str,
        eraser: Annotated[AuthorDelete, Depends(get_author_eraser)]
) -> None:
    """Delete an author by their ID, ensuring they are not associated with any books."""
    try:
        await eraser.dispatch(author_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AuthorBookAssociatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    'get_authors',
    'create_author',
    'get_author',
    'update_author',
    'delete_author',
]
