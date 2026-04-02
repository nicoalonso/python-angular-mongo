import pytest
from fastapi import HTTPException

from src.application.purchase.creator import PurchaseCreate, PurchaseCreatePayload
from src.application.purchase.eraser import PurchaseDelete
from src.application.purchase.list import PurchaseQueryPayload, PurchaseList
from src.application.purchase.reader import PurchaseRead
from src.application.purchase.updater import PurchaseUpdatePayload, PurchaseUpdate
from src.infrastructure.controller.v1.purchase_controller import *
from tests.doubles.infrastructure.bus import DomainBusStub
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import Ref, FixturePayload


@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_provider_repository():
    return ProviderRepositoryStub()

@pytest.fixture()
def my_book_repository():
    return BookRepositoryStub()

@pytest.fixture()
def my_purchase_repository(my_provider_repository):
    return PurchaseRepositoryStub(repo_provider=my_provider_repository)

@pytest.fixture()
def my_purchase_line_repository(my_purchase_repository, my_book_repository):
    return PurchaseLineRepositoryStub(
        repo_purchase=my_purchase_repository,
        repo_book=my_book_repository,
    )

@pytest.fixture()
def my_purchase_lister(my_purchase_repository):
    return PurchaseList(my_purchase_repository)

@pytest.fixture()
def my_purchase_creator(
        my_purchase_repository,
        my_purchase_line_repository,
        my_provider_repository,
        my_book_repository,
):
    repo_user = UserRepositoryStub()
    bus = DomainBusStub()
    return PurchaseCreate(
        my_purchase_repository,
        my_purchase_line_repository,
        my_provider_repository,
        my_book_repository,
        repo_user,
        bus,
    )

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('purchase')
    return PurchaseCreatePayload(**data)

@pytest.fixture()
def my_purchase_reader(my_purchase_repository, my_purchase_line_repository):
    return PurchaseRead(my_purchase_repository, my_purchase_line_repository)

@pytest.fixture()
def my_purchase_updater(
        my_purchase_repository,
        my_purchase_line_repository,
        my_provider_repository,
        my_book_repository,
):
    repo_user = UserRepositoryStub()
    bus = DomainBusStub()
    return PurchaseUpdate(
        my_purchase_repository,
        my_purchase_line_repository,
        my_provider_repository,
        my_book_repository,
        repo_user,
        bus,
    )

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('purchase')
    return PurchaseUpdatePayload(**data)

@pytest.fixture()
def my_purchase_eraser(my_purchase_repository, my_purchase_line_repository):
    bus = DomainBusStub()
    return PurchaseDelete(
        my_purchase_repository,
        my_purchase_line_repository,
        bus,
    )


# get_purchases
@pytest.mark.asyncio
async def test_get_purchases_should_fail_when_wrong_field(my_purchase_lister):
    query = PurchaseQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_purchases(query, my_purchase_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_purchases_should_fail_when_server_error(my_purchase_repository, my_purchase_lister):
    my_purchase_repository.error('Database connection error')
    query = PurchaseQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_purchases(query, my_purchase_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_purchases_should_run(my_purchase_repository, my_purchase_lister):
    my_purchase_repository.attach_all()
    query = PurchaseQueryPayload()

    result = await get_purchases(query, my_purchase_lister)

    assert len(result.items) > 0

# create_purchase
@pytest.mark.asyncio
async def test_create_purchase_should_fail_when_book_not_found(my_purchase_creator, my_payload_create):
    with pytest.raises(HTTPException) as exc:
        await create_purchase(my_payload_create, my_purchase_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_purchase_should_fail_when_server_error(my_book_repository, my_purchase_creator, my_payload_create):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_purchase(my_payload_create, my_purchase_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_purchase_should_run_when_create(
        my_purchase_repository,
        my_book_repository,
        my_provider_repository,
        my_purchase_creator,
        my_payload_create
):
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_provider_repository.put(Ref.ProviderBestBuy)

    await create_purchase(my_payload_create, my_purchase_creator)

    assert my_purchase_repository.stored is not None

# get_purchase
@pytest.mark.asyncio
async def test_get_purchase_should_fail_when_not_found(my_purchase_reader):
    with pytest.raises(HTTPException) as exc:
        await get_purchase('not-exists', my_purchase_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_purchase_should_fail_when_server_error(my_purchase_repository, my_purchase_reader):
    my_purchase_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_purchase('12355', my_purchase_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_purchase_should_read(
        my_purchase_repository,
        my_purchase_line_repository,
        my_purchase_reader,
):
    my_purchase_repository.put(Ref.PurchaseAmazonInv1)
    my_purchase_line_repository.attach(Ref.PurchaseLineAmazonLine1)

    view = await get_purchase('12355', my_purchase_reader)

    assert len(view.data.lines) == 1

# update_purchase
@pytest.mark.asyncio
async def test_update_purchase_should_fail_when_not_found(my_purchase_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_purchase('1235465', my_payload_update, my_purchase_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_purchase_should_fail_when_bad_request(my_purchase_repository, my_purchase_updater, my_payload_update):
    my_purchase_repository.put(Ref.PurchaseAmazonInv1)

    with pytest.raises(HTTPException) as exc:
        await update_purchase('1235465', my_payload_update, my_purchase_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_purchase_should_fail_when_server_error(my_purchase_repository, my_purchase_updater, my_payload_update):
    my_purchase_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_purchase('1235465', my_payload_update, my_purchase_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_purchase_should_run_when_update(
        my_purchase_repository,
        my_book_repository,
        my_provider_repository,
        my_purchase_updater,
        my_payload_update
):
    my_purchase_repository.put(Ref.PurchaseAmazonInv1)
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_provider_repository.put(Ref.ProviderBestBuy)

    await update_purchase('1235465', my_payload_update, my_purchase_updater)

    assert my_purchase_repository.stored is not None

# delete_purchase
@pytest.mark.asyncio
async def test_delete_purchase_should_fail_when_not_found(my_purchase_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_purchase('not-exists', my_purchase_eraser)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_purchase_should_fail_server_error(my_purchase_eraser, my_purchase_repository):
    my_purchase_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_purchase('not-exists', my_purchase_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_purchase_should_run_when_delete(my_purchase_eraser, my_purchase_repository):
    my_purchase_repository.put(Ref.PurchaseAmazonInv1)

    await delete_purchase('not-exists', my_purchase_eraser)

    assert my_purchase_repository.removed is not None
