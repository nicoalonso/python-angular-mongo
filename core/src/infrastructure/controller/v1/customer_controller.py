from typing import Annotated

from fastapi import Query, Depends, HTTPException

from src.domain.identity.exception import BadRequestError, NotFoundError
from src.domain.identity.list import ListQuery
from src.application.customer.creator import CustomerCreatePayload, CustomerCreate
from src.application.customer.eraser import CustomerDelete, CustomerAssociatedError
from src.application.customer.list import CustomerQueryPayload, CustomerList
from src.application.customer.reader import CustomerRead
from src.application.customer.updater import CustomerUpdatePayload, CustomerUpdate
from src.infrastructure.dependencies.customer import *
from src.infrastructure.router import router
from src.presentation.identity import ListView
from src.presentation.v1.customer import CustomerReadViewData, CustomerReadView


@router.get("/customers", tags=["Customers"], summary='Get all customers')
async def get_customers(
        query_params: Annotated[CustomerQueryPayload, Query()],
        lister: Annotated[CustomerList, Depends(get_customer_list)]
) -> ListView[CustomerReadViewData]:
    """Get a list of customers with optional filters, pagination, and sorting."""
    try:
        query = ListQuery.parse(query_params)
        result = await lister.dispatch(query)
        return ListView.serialize(result, CustomerReadViewData)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customers", tags=["Customers"], status_code=201, summary='Create a new customer')
async def create_customer(
        payload: CustomerCreatePayload,
        creator: Annotated[CustomerCreate, Depends(get_customer_creator)],
) -> CustomerReadView:
    """Create a new customer with the provided details."""
    try:
        customer = await creator.dispatch(payload)
        return CustomerReadView(customer)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers/{customer_id}", tags=["Customers"], summary='Get a customer by ID')
async def get_customer(
        customer_id: str,
        reader: Annotated[CustomerRead, Depends(get_customer_reader)]
) -> CustomerReadView:
    """Retrieve a customer by their unique identifier."""
    try:
        customer = await reader.dispatch(customer_id)
        return CustomerReadView(customer)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/customers/{customer_id}", tags=["Customers"], status_code=204, summary='Update a customer by ID')
async def update_customer(
        customer_id: str,
        payload: CustomerUpdatePayload,
        updater: Annotated[CustomerUpdate, Depends(get_customer_updater)],
) -> None:
    """Update an existing customer's details by their unique identifier."""
    try:
        await updater.dispatch(customer_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/customers/{customer_id}", tags=["Customers"], status_code=204, summary='Delete a customer by ID')
async def delete_customer(
        customer_id: str,
        eraser: Annotated[CustomerDelete, Depends(get_customer_eraser)]
) -> None:
    """Delete a customer by their unique identifier."""
    try:
        await eraser.dispatch(customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CustomerAssociatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    'get_customers',
    'create_customer',
    'get_customer',
    'update_customer',
    'delete_customer',
]
