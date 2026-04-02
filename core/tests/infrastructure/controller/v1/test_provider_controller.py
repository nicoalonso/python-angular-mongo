import pytest
from fastapi import HTTPException

from src.application.provider.creator import ProviderCreate, ProviderCreatePayload
from src.application.provider.eraser import ProviderDelete
from src.application.provider.list import ProviderQueryPayload, ProviderList
from src.application.provider.reader import ProviderRead
from src.application.provider.updater import ProviderUpdate, ProviderUpdatePayload
from src.infrastructure.controller.v1.provider_controller import *
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub, UserRepositoryStub, PurchaseRepositoryStub
from tests.fixtures import Ref, FixturePayload


@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_provider_repository():
    return ProviderRepositoryStub()

@pytest.fixture()
def my_purchase_repository(my_provider_repository):
    return PurchaseRepositoryStub(repo_provider=my_provider_repository)

@pytest.fixture()
def my_provider_lister(my_provider_repository):
    return ProviderList(my_provider_repository)

@pytest.fixture()
def my_provider_creator(my_provider_repository):
    repo_user = UserRepositoryStub()
    return ProviderCreate(my_provider_repository, repo_user)

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('provider')
    return ProviderCreatePayload(**data)

@pytest.fixture()
def my_provider_reader(my_provider_repository):
    return ProviderRead(my_provider_repository)

@pytest.fixture()
def my_provider_updater(my_provider_repository):
    repo_user = UserRepositoryStub()
    return ProviderUpdate(my_provider_repository, repo_user)

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('provider')
    return ProviderUpdatePayload(**data)

@pytest.fixture()
def my_provider_eraser(my_provider_repository, my_purchase_repository):
    return ProviderDelete(my_provider_repository, my_purchase_repository)



# get_providers
@pytest.mark.asyncio
async def test_get_providers_should_fail_when_wrong_field(my_provider_lister):
    query = ProviderQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_providers(query, my_provider_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_providers_should_fail_when_server_error(my_provider_repository, my_provider_lister):
    my_provider_repository.error('Database connection error')
    query = ProviderQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_providers(query, my_provider_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_providers_should_run(my_provider_repository, my_provider_lister):
    my_provider_repository.attach_all()
    query = ProviderQueryPayload()

    result = await get_providers(query, my_provider_lister)

    assert len(result.items) > 0

# create_provider
@pytest.mark.asyncio
async def test_create_provider_should_fail_when_already_exists(my_provider_repository, my_provider_creator, my_payload_create):
    my_provider_repository.put(Ref.ProviderBestBuy)

    with pytest.raises(HTTPException) as exc:
        await create_provider(my_payload_create, my_provider_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_provider_should_fail_when_server_error(my_provider_repository, my_provider_creator, my_payload_create):
    my_provider_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_provider(my_payload_create, my_provider_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_provider_should_run_when_create(my_provider_repository, my_provider_creator, my_payload_create):
    await create_provider(my_payload_create, my_provider_creator)

    assert my_provider_repository.stored is not None

# get_provider
@pytest.mark.asyncio
async def test_get_provider_should_fail_when_not_found(my_provider_reader):
    with pytest.raises(HTTPException) as exc:
        await get_provider('not-exists', my_provider_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_provider_should_fail_when_server_error(my_provider_repository, my_provider_reader):
    my_provider_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_provider('12355', my_provider_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_provider_should_read(my_provider_repository, my_provider_reader):
    my_provider_repository.put(Ref.ProviderAmazon)

    view = await get_provider('12355', my_provider_reader)

    assert view.data.name == 'Amazon'

# update_provider
@pytest.mark.asyncio
async def test_update_provider_should_fail_when_not_found(my_provider_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_provider('1235465', my_payload_update, my_provider_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_provider_should_fail_when_bad_request(my_provider_repository, my_provider_updater, my_payload_update):
    my_provider_repository.put(Ref.ProviderBestBuy)
    my_payload_update.name = ''  # Invalid name

    with pytest.raises(HTTPException) as exc:
        await update_provider('1235465', my_payload_update, my_provider_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_provider_should_fail_when_server_error(my_provider_repository, my_provider_updater, my_payload_update):
    my_provider_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_provider('1235465', my_payload_update, my_provider_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_provider_should_run_when_update(my_provider_repository, my_provider_updater, my_payload_update):
    my_provider_repository.put(Ref.ProviderBestBuy)

    await update_provider('1235465', my_payload_update, my_provider_updater)

    assert my_provider_repository.stored is not None

# delete_provider
@pytest.mark.asyncio
async def test_delete_provider_should_fail_when_not_found(my_provider_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_provider('not-exists', my_provider_eraser)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_provider_should_bad_request(my_provider_eraser, my_provider_repository, my_purchase_repository):
    my_provider_repository.put(Ref.ProviderAmazon)
    my_purchase_repository.attach(Ref.PurchaseAmazonInv1)

    with pytest.raises(HTTPException) as exc:
        await delete_provider('12356', my_provider_eraser)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_delete_provider_should_fail_server_error(my_provider_eraser, my_provider_repository):
    my_provider_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_provider('12356', my_provider_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_provider_should_run_when_delete(my_provider_eraser, my_provider_repository):
    my_provider_repository.put(Ref.ProviderAmazon)

    await delete_provider('12356', my_provider_eraser)

    assert my_provider_repository.removed is not None
