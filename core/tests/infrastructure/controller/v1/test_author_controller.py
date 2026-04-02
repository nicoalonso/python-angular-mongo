import pytest
from fastapi import HTTPException

from src.application.author.creator import AuthorCreate, AuthorCreatePayload
from src.application.author.eraser import AuthorDelete
from src.application.author.list import AuthorQueryPayload, AuthorList
from src.application.author.reader import AuthorRead
from src.application.author.updater import AuthorUpdate, AuthorUpdatePayload
from src.infrastructure.controller.v1.author_controller import *
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub, UserRepositoryStub, BookRepositoryStub
from tests.fixtures import Ref, FixturePayload


@pytest.fixture()
def my_author_repository():
    return AuthorRepositoryStub()

@pytest.fixture()
def my_book_repository():
    return BookRepositoryStub()

@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_author_lister(my_author_repository):
    return AuthorList(my_author_repository)

@pytest.fixture()
def my_author_creator(my_author_repository):
    repo_user = UserRepositoryStub()
    return AuthorCreate(my_author_repository, repo_user)

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('author')
    return AuthorCreatePayload(**data)

@pytest.fixture()
def my_author_reader(my_author_repository):
    return AuthorRead(my_author_repository)

@pytest.fixture()
def my_author_updater(my_author_repository):
    repo_user = UserRepositoryStub()
    return AuthorUpdate(my_author_repository, repo_user)

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('author')
    return AuthorUpdatePayload(**data)

@pytest.fixture()
def my_author_eraser(my_author_repository, my_book_repository):
    return AuthorDelete(my_author_repository, my_book_repository)


# get_authors
@pytest.mark.asyncio
async def test_get_authors_should_fail_when_wrong_field(my_author_lister):
    query = AuthorQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_authors(query, my_author_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_authors_should_fail_when_server_error(my_author_repository, my_author_lister):
    my_author_repository.error('Database connection error')
    query = AuthorQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_authors(query, my_author_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_authors_should_run(my_author_repository, my_author_lister):
    my_author_repository.attach_all()
    query = AuthorQueryPayload()

    result = await get_authors(query, my_author_lister)

    assert len(result.items) > 0

# create_author
@pytest.mark.asyncio
async def test_create_author_should_fail_when_already_exists(my_author_repository, my_author_creator, my_payload_create):
    my_author_repository.put(Ref.AuthorShakespeare)

    with pytest.raises(HTTPException) as exc:
        await create_author(my_payload_create, my_author_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_author_should_fail_when_server_error(my_author_repository, my_author_creator, my_payload_create):
    my_author_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_author(my_payload_create, my_author_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_author_should_run_when_create(my_author_repository, my_author_creator, my_payload_create):
    await create_author(my_payload_create, my_author_creator)

    assert my_author_repository.stored is not None

# get_author
@pytest.mark.asyncio
async def test_get_author_should_fail_when_not_found(my_author_reader):
    with pytest.raises(HTTPException) as exc:
        await get_author('not-exists', my_author_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_author_should_fail_when_server_error(my_author_repository, my_author_reader):
    my_author_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_author('12355', my_author_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_author_should_read(my_author_repository, my_author_reader):
    my_author_repository.put(Ref.AuthorShakespeare)

    view = await get_author('12355', my_author_reader)

    assert view.data.name == 'William Shakespeare'

# update_author
@pytest.mark.asyncio
async def test_update_author_should_fail_when_not_found(my_author_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_author('1235465', my_payload_update, my_author_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_author_should_fail_when_bad_request(my_author_repository, my_author_updater, my_payload_update):
    my_author_repository.put(Ref.AuthorCervantes)
    my_payload_update.name = ''  # Invalid name

    with pytest.raises(HTTPException) as exc:
        await update_author('1235465', my_payload_update, my_author_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_author_should_fail_when_server_error(my_author_repository, my_author_updater, my_payload_update):
    my_author_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_author('1235465', my_payload_update, my_author_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_author_should_run_when_update(my_author_repository, my_author_updater, my_payload_update):
    my_author_repository.put(Ref.AuthorCervantes)

    await update_author('1235465', my_payload_update, my_author_updater)

    assert my_author_repository.stored is not None

# delete_author
@pytest.mark.asyncio
async def test_delete_author_should_fail_when_not_found(my_author_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_author('not-exists', my_author_eraser)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_author_should_fail_when_bad_request(
        my_author_eraser,
        my_book_repository,
        my_author_repository
):
    my_author_repository.put(Ref.AuthorCervantes)
    my_book_repository.attach(Ref.BookDonQuijote)

    with pytest.raises(HTTPException) as exc:
        await delete_author('not-exists', my_author_eraser)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_delete_author_should_fail_server_error(my_author_eraser, my_author_repository):
    my_author_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_author('not-exists', my_author_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_author_should_run_when_delete(my_author_eraser, my_author_repository):
    my_author_repository.put(Ref.AuthorCervantes)

    await delete_author('not-exists', my_author_eraser)

    assert my_author_repository.removed is not None
