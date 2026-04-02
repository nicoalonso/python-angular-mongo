import pytest
from fastapi import HTTPException

from src.application.editorial.creator import EditorialCreate, EditorialCreatePayload
from src.application.editorial.eraser import EditorialDelete
from src.application.editorial.list import EditorialList, EditorialQueryPayload
from src.application.editorial.reader import EditorialRead
from src.application.editorial.updater import EditorialUpdate, EditorialUpdatePayload
from src.infrastructure.controller.v1.editorial_controller import *
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub, UserRepositoryStub, BookRepositoryStub
from tests.fixtures import Ref, FixturePayload

@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_editorial_repository():
    return EditorialRepositoryStub()

@pytest.fixture()
def my_book_repository():
    return BookRepositoryStub()

@pytest.fixture()
def my_editorial_lister(my_editorial_repository):
    return EditorialList(my_editorial_repository)

@pytest.fixture()
def my_editorial_creator(my_editorial_repository):
    repo_user = UserRepositoryStub()
    return EditorialCreate(my_editorial_repository, repo_user)

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('editorial')
    return EditorialCreatePayload(**data)

@pytest.fixture()
def my_editorial_reader(my_editorial_repository):
    return EditorialRead(my_editorial_repository)

@pytest.fixture()
def my_editorial_updater(my_editorial_repository):
    repo_user = UserRepositoryStub()
    return EditorialUpdate(my_editorial_repository, repo_user)

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('editorial')
    return EditorialUpdatePayload(**data)

@pytest.fixture()
def my_editorial_eraser(my_editorial_repository, my_book_repository):
    return EditorialDelete(my_editorial_repository, my_book_repository)


# get_editorials
@pytest.mark.asyncio
async def test_get_editorials_should_fail_when_wrong_field(my_editorial_lister):
    query = EditorialQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_editorials(query, my_editorial_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_editorials_should_fail_when_server_error(my_editorial_repository, my_editorial_lister):
    my_editorial_repository.error('Database connection error')
    query = EditorialQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_editorials(query, my_editorial_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_editorials_should_run(my_editorial_repository, my_editorial_lister):
    my_editorial_repository.attach_all()
    query = EditorialQueryPayload()

    result = await get_editorials(query, my_editorial_lister)

    assert len(result.items) > 0

# create_editorial
@pytest.mark.asyncio
async def test_create_editorial_should_fail_when_already_exists(my_editorial_repository, my_editorial_creator, my_payload_create):
    my_editorial_repository.put(Ref.EditorialAnaya)

    with pytest.raises(HTTPException) as exc:
        await create_editorial(my_payload_create, my_editorial_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_editorial_should_fail_when_server_error(my_editorial_repository, my_editorial_creator, my_payload_create):
    my_editorial_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_editorial(my_payload_create, my_editorial_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_editorial_should_run_when_create(my_editorial_repository, my_editorial_creator, my_payload_create):
    await create_editorial(my_payload_create, my_editorial_creator)

    assert my_editorial_repository.stored is not None

# get_editorial
@pytest.mark.asyncio
async def test_get_editorial_should_fail_when_not_found(my_editorial_reader):
    with pytest.raises(HTTPException) as exc:
        await get_editorial('not-exists', my_editorial_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_editorial_should_fail_when_server_error(my_editorial_repository, my_editorial_reader):
    my_editorial_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_editorial('12355', my_editorial_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_editorial_should_read(my_editorial_repository, my_editorial_reader):
    my_editorial_repository.put(Ref.EditorialAnaya)

    view = await get_editorial('12355', my_editorial_reader)

    assert view.data.name == 'Anaya'

# update_editorial
@pytest.mark.asyncio
async def test_update_editorial_should_fail_when_not_found(my_editorial_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_editorial('1235465', my_payload_update, my_editorial_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_editorial_should_fail_when_bad_request(my_editorial_repository, my_editorial_updater, my_payload_update):
    my_editorial_repository.put(Ref.EditorialAnaya)
    my_payload_update.name = ''  # Invalid name

    with pytest.raises(HTTPException) as exc:
        await update_editorial('1235465', my_payload_update, my_editorial_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_editorial_should_fail_when_server_error(my_editorial_repository, my_editorial_updater, my_payload_update):
    my_editorial_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_editorial('1235465', my_payload_update, my_editorial_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_editorial_should_run_when_update(my_editorial_repository, my_editorial_updater, my_payload_update):
    my_editorial_repository.put(Ref.EditorialAnaya)

    await update_editorial('1235465', my_payload_update, my_editorial_updater)

    assert my_editorial_repository.stored is not None

# delete_editorial
@pytest.mark.asyncio
async def test_delete_editorial_should_fail_when_not_found(my_editorial_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_editorial('not-exists', my_editorial_eraser)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_editorial_should_bad_request(my_editorial_eraser, my_editorial_repository, my_book_repository):
    my_editorial_repository.put(Ref.EditorialAnaya)
    my_book_repository.attach(Ref.BookDonQuijote)

    with pytest.raises(HTTPException) as exc:
        await delete_editorial('12356', my_editorial_eraser)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_delete_editorial_should_fail_server_error(my_editorial_eraser, my_editorial_repository):
    my_editorial_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_editorial('12356', my_editorial_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_editorial_should_run_when_delete(my_editorial_eraser, my_editorial_repository):
    my_editorial_repository.put(Ref.EditorialAnaya)

    await delete_editorial('12356', my_editorial_eraser)

    assert my_editorial_repository.removed is not None
