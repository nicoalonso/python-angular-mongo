from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Query, Depends

from src.domain.book.exception import BookNotFoundError
from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.book.available import BookAvailable, BookAvailableQueryPayload
from src.application.book.creator import BookCreatePayload, BookCreate
from src.application.book.eraser import BookDelete
from src.application.book.list import BookQueryPayload, BookList
from src.application.book.reader import BookRead
from src.application.book.updater import BookUpdate, BookUpdatePayload
from src.infrastructure.dependencies.book import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.book import BookReadViewData, BookReadView, BookAvailableView


@router.get("/books", tags=["Books"], summary='Get all books')
async def get_books(
        query_params: Annotated[BookQueryPayload, Query()],
        lister: Annotated[BookList, Depends(get_book_lister)]
) -> ListView[BookReadViewData]:
    """Get a list of books with optional filters and pagination."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, BookReadViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/books", tags=["Books"], status_code=201, summary='Create a new book')
async def create_book(
        payload: BookCreatePayload,
        creator: Annotated[BookCreate, Depends(get_book_creator)],
) -> BookReadView:
    """Create a new book with the provided details."""
    try:
        book = await creator.dispatch(payload)
        return BookReadView(book)
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books/{book_id}", tags=["Books"], summary='Get a book by ID')
async def get_book(
        book_id: str,
        reader: Annotated[BookRead, Depends(get_book_reader)]
) -> BookReadView:
    """Get a book by its unique identifier."""
    try:
        book = await reader.dispatch(book_id)
        return BookReadView(book)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/books/{book_id}", tags=["Books"], status_code=204, summary='Update a book by ID')
async def update_book(
        book_id: str,
        payload: BookUpdatePayload,
        updater: Annotated[BookUpdate, Depends(get_book_updater)],
) -> None:
    """Update an existing book's details by its unique identifier."""
    try:
        await updater.dispatch(book_id, payload)
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (BadRequestError, NotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/books/{book_id}", tags=["Books"], status_code=204, summary='Delete a book by ID')
async def delete_book(
        book_id: str,
        eraser: Annotated[BookDelete, Depends(get_book_eraser)]
) -> None:
    """Delete a book by its unique identifier."""
    try:
        await eraser.dispatch(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books/{book_id}/available", tags=["Books"], summary='Check if a book is available')
async def book_available(
        book_id: str,
        payload: Annotated[BookAvailableQueryPayload, Query()],
        available: Annotated[BookAvailable, Depends(get_book_available)],
) -> BookAvailableView:
    """Check if a book is available for sale or rent by its unique identifier."""
    try:
        is_available = await available.dispatch(book_id, payload.is_sale)
        return BookAvailableView(is_available)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    'get_books',
    'create_book',
    'get_book',
    'update_book',
    'delete_book',
    'book_available',
]
