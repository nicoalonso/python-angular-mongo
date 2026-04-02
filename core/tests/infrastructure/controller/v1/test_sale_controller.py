import pytest
from fastapi import HTTPException

from src.application.sale.creator import SaleCreate, SaleCreatePayload
from src.application.sale.list import SaleQueryPayload, SaleList
from src.application.sale.reader import SaleRead
from src.infrastructure.controller.v1.sale_controller import *
from tests.doubles.infrastructure.bus import DomainBusStub
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_customer_repository():
    return CustomerRepositoryStub()

@pytest.fixture()
def my_book_repository():
    return BookRepositoryStub()

@pytest.fixture()
def my_sale_repository(my_customer_repository):
    return SaleRepositoryStub(repo_customer=my_customer_repository)

@pytest.fixture()
def my_sale_line_repository(my_sale_repository, my_book_repository):
    return SaleLineRepositoryStub(
        repo_sale=my_sale_repository,
        repo_book=my_book_repository,
    )

@pytest.fixture()
def my_sale_lister(my_sale_repository):
    return SaleList(my_sale_repository)

@pytest.fixture()
def my_sale_creator(
        my_sale_repository,
        my_sale_line_repository,
        my_customer_repository,
        my_book_repository,
):
    repo_sequence_number = SequenceNumberRepositoryStub()
    repo_user = UserRepositoryStub()
    bus = DomainBusStub()
    return SaleCreate(
        my_sale_repository,
        my_sale_line_repository,
        my_customer_repository,
        my_book_repository,
        repo_sequence_number,
        repo_user,
        bus,
    )

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('sale')
    return SaleCreatePayload(**data)

@pytest.fixture()
def my_sale_reader(my_sale_repository, my_sale_line_repository):
    return SaleRead(my_sale_repository, my_sale_line_repository)


# get_sales
@pytest.mark.asyncio
async def test_get_sales_should_fail_when_wrong_field(my_sale_lister):
    query = SaleQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_sales(query, my_sale_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_sales_should_fail_when_server_error(my_sale_repository, my_sale_lister):
    my_sale_repository.error('Database connection error')
    query = SaleQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_sales(query, my_sale_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_sales_should_run(my_sale_repository, my_sale_lister):
    my_sale_repository.attach_all()
    query = SaleQueryPayload()

    result = await get_sales(query, my_sale_lister)

    assert len(result.items) > 0

# create_sale
@pytest.mark.asyncio
async def test_create_sale_should_fail_when_book_not_found(my_sale_creator, my_payload_create):
    with pytest.raises(HTTPException) as exc:
        await create_sale(my_payload_create, my_sale_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_sale_should_fail_when_server_error(my_book_repository, my_sale_creator, my_payload_create):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_sale(my_payload_create, my_sale_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_sale_should_run_when_create(
        my_sale_repository,
        my_book_repository,
        my_customer_repository,
        my_sale_creator,
        my_payload_create
):
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_customer_repository.put(Ref.CustomerJohnDoe)

    await create_sale(my_payload_create, my_sale_creator)

    assert my_sale_repository.stored is not None

# get_sale
@pytest.mark.asyncio
async def test_get_sale_should_fail_when_not_found(my_sale_reader):
    with pytest.raises(HTTPException) as exc:
        await get_sale('not-exists', my_sale_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_sale_should_fail_when_server_error(my_sale_repository, my_sale_reader):
    my_sale_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_sale('12355', my_sale_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_sale_should_read(
        my_sale_repository,
        my_sale_line_repository,
        my_sale_reader,
):
    my_sale_repository.put(Ref.SaleJohnDoe1)
    my_sale_line_repository.attach(Ref.SaleLineJohnDoe1Line1)

    view = await get_sale('12355', my_sale_reader)

    assert len(view.data.lines) == 1
