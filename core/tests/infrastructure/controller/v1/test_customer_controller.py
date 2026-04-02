import pytest
from fastapi import HTTPException

from src.application.customer.creator import CustomerCreatePayload, CustomerCreate
from src.application.customer.eraser import CustomerDelete
from src.application.customer.list import CustomerList, CustomerQueryPayload
from src.application.customer.reader import CustomerRead
from src.application.customer.updater import CustomerUpdatePayload, CustomerUpdate
from src.infrastructure.controller.v1.customer_controller import *
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import Ref, FixturePayload


@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_customer_repository():
    return CustomerRepositoryStub()

@pytest.fixture()
def my_customer_lister(my_customer_repository):
    return CustomerList(my_customer_repository)

@pytest.fixture()
def my_customer_creator(my_customer_repository):
    repo_sequence = SequenceNumberRepositoryStub()
    repo_user = UserRepositoryStub()
    return CustomerCreate(my_customer_repository, repo_sequence, repo_user)

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('customer-create')
    return CustomerCreatePayload(**data)

@pytest.fixture()
def my_customer_reader(my_customer_repository):
    return CustomerRead(my_customer_repository)

@pytest.fixture()
def my_customer_updater(my_customer_repository):
    repo_user = UserRepositoryStub()
    return CustomerUpdate(my_customer_repository, repo_user)

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('customer-update')
    return CustomerUpdatePayload(**data)

@pytest.fixture()
def my_customer_eraser(my_customer_repository):
    repo_sale = SaleRepositoryStub(repo_customer=my_customer_repository)
    repo_borrow = BorrowRepositoryStub(repo_customer=my_customer_repository)
    return CustomerDelete(
        my_customer_repository,
        repo_sale,
        repo_borrow,
    )


# get_customers
@pytest.mark.asyncio
async def test_get_customers_should_fail_when_wrong_field(my_customer_lister):
    query = CustomerQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_customers(query, my_customer_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_customers_should_fail_when_server_error(my_customer_repository, my_customer_lister):
    my_customer_repository.error('Database connection error')
    query = CustomerQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_customers(query, my_customer_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_customers_should_run(my_customer_repository, my_customer_lister):
    my_customer_repository.attach_all()
    query = CustomerQueryPayload()

    result = await get_customers(query, my_customer_lister)

    assert len(result.items) > 0

# create_customer
@pytest.mark.asyncio
async def test_create_customer_should_fail_when_already_exists(my_customer_repository, my_customer_creator, my_payload_create):
    my_customer_repository.put(Ref.CustomerJohnDoe)

    with pytest.raises(HTTPException) as exc:
        await create_customer(my_payload_create, my_customer_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_customer_should_fail_when_server_error(my_customer_repository, my_customer_creator, my_payload_create):
    my_customer_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_customer(my_payload_create, my_customer_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_customer_should_run_when_create(my_customer_repository, my_customer_creator, my_payload_create):
    await create_customer(my_payload_create, my_customer_creator)

    assert my_customer_repository.stored is not None

# get_customer
@pytest.mark.asyncio
async def test_get_customer_should_fail_when_not_found(my_customer_reader):
    with pytest.raises(HTTPException) as exc:
        await get_customer('not-exists', my_customer_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_customer_should_fail_when_server_error(my_customer_repository, my_customer_reader):
    my_customer_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_customer('12355', my_customer_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_customer_should_read(my_customer_repository, my_customer_reader):
    my_customer_repository.put(Ref.CustomerJohnDoe)

    view = await get_customer('12355', my_customer_reader)

    assert view.data.name == 'John'

# update_customer
@pytest.mark.asyncio
async def test_update_customer_should_fail_when_not_found(my_customer_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_customer('1235465', my_payload_update, my_customer_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_customer_should_fail_when_bad_request(my_customer_repository, my_customer_updater, my_payload_update):
    my_customer_repository.put(Ref.CustomerJohnDoe)
    my_payload_update.name = ''  # Invalid name

    with pytest.raises(HTTPException) as exc:
        await update_customer('1235465', my_payload_update, my_customer_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_customer_should_fail_when_server_error(my_customer_repository, my_customer_updater, my_payload_update):
    my_customer_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_customer('1235465', my_payload_update, my_customer_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_customer_should_run_when_update(my_customer_repository, my_customer_updater, my_payload_update):
    my_customer_repository.put(Ref.CustomerJohnDoe)

    await update_customer('1235465', my_payload_update, my_customer_updater)

    assert my_customer_repository.stored is not None

# delete_customer
@pytest.mark.asyncio
async def test_delete_customer_should_fail_when_not_found(my_customer_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_customer('not-exists', my_customer_eraser)

    assert exc.value.status_code == 404

# @pytest.mark.asyncio
# async def test_delete_customer_should_bad_request(my_customer_eraser, my_customer_repository):
#     my_customer_repository.put(Ref.ProviderAmazon)
#
#     with pytest.raises(HTTPException) as exc:
#         await delete_customer('12356', my_customer_eraser)
#
#     assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_delete_customer_should_fail_server_error(my_customer_eraser, my_customer_repository):
    my_customer_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_customer('12356', my_customer_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_customer_should_run_when_delete(my_customer_eraser, my_customer_repository):
    my_customer_repository.put(Ref.CustomerJohnDoe)

    await delete_customer('12356', my_customer_eraser)

    assert my_customer_repository.removed is not None
