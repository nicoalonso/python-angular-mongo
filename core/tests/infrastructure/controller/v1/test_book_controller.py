import pytest
from fastapi import HTTPException

from src.application.book.available import BookAvailableQueryPayload, BookAvailable
from src.application.book.creator import BookCreate, BookCreatePayload
from src.application.book.eraser import BookDelete
from src.application.book.list import BookList, BookQueryPayload
from src.application.book.reader import BookRead
from src.application.book.updater import BookUpdate, BookUpdatePayload
from src.domain.services.book_inspector import BookInspectFactory
from src.infrastructure.controller.v1.book_controller import *
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import Ref, FixturePayload


@pytest.fixture()
def my_loader():
    return FixturePayload()

@pytest.fixture()
def my_book_repository():
    return BookRepositoryStub()

@pytest.fixture()
def my_author_repository():
    return AuthorRepositoryStub()

@pytest.fixture()
def my_editorial_repository():
    return EditorialRepositoryStub()

@pytest.fixture()
def my_book_lister(my_book_repository):
    return BookList(my_book_repository)

@pytest.fixture()
def my_book_creator(my_book_repository, my_author_repository, my_editorial_repository):
    repo_user = UserRepositoryStub()
    return BookCreate(my_book_repository, my_author_repository, my_editorial_repository, repo_user)

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('book')
    return BookCreatePayload(**data)

@pytest.fixture()
def my_book_reader(my_book_repository):
    return BookRead(my_book_repository)

@pytest.fixture()
def my_book_updater(my_book_repository, my_author_repository, my_editorial_repository):
    repo_user = UserRepositoryStub()
    return BookUpdate(my_book_repository, my_author_repository, my_editorial_repository, repo_user)

@pytest.fixture()
def my_payload_update(my_loader):
    data = my_loader.load('book')
    return BookUpdatePayload(**data)

@pytest.fixture()
def my_book_eraser(my_book_repository):
    repo_purchase_line = PurchaseLineRepositoryStub()
    repo_sale_line = SaleLineRepositoryStub()
    repo_borrow_line = BorrowLineRepositoryStub()
    return BookDelete(
        my_book_repository,
        repo_purchase_line,
        repo_sale_line,
        repo_borrow_line
    )

@pytest.fixture()
def my_book_available(my_book_repository):
    my_borrow_line_repository = BorrowLineRepositoryStub()
    factory = BookInspectFactory(my_borrow_line_repository)
    return BookAvailable(my_book_repository, factory)


# get_books
@pytest.mark.asyncio
async def test_get_books_should_fail_when_wrong_field(my_book_lister):
    query = BookQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_books(query, my_book_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_books_should_fail_when_server_error(my_book_repository, my_book_lister):
    my_book_repository.error('Database connection error')
    query = BookQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_books(query, my_book_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_books_should_run(my_book_repository, my_book_lister):
    my_book_repository.attach_all()
    query = BookQueryPayload()

    result = await get_books(query, my_book_lister)

    assert len(result.items) > 0

# create_book
@pytest.mark.asyncio
async def test_create_book_should_fail_when_already_exists(my_book_repository, my_book_creator, my_payload_create):
    my_book_repository.put(Ref.BookRomeoAndJuliet)

    with pytest.raises(HTTPException) as exc:
        await create_book(my_payload_create, my_book_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_book_should_fail_when_author_not_found(my_book_creator, my_payload_create):
    with pytest.raises(HTTPException) as exc:
        await create_book(my_payload_create, my_book_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_book_should_fail_when_server_error(my_book_repository, my_book_creator, my_payload_create):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_book(my_payload_create, my_book_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_book_should_run_when_create(
        my_book_repository,
        my_author_repository,
        my_editorial_repository,
        my_book_creator,
        my_payload_create,
):
    my_author_repository.put(Ref.AuthorShakespeare)
    my_editorial_repository.put(Ref.EditorialAnaya)

    await create_book(my_payload_create, my_book_creator)

    assert my_book_repository.stored is not None

# get_book
@pytest.mark.asyncio
async def test_get_book_should_fail_when_not_found(my_book_reader):
    with pytest.raises(HTTPException) as exc:
        await get_book('not-exists', my_book_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_book_should_fail_when_server_error(my_book_repository, my_book_reader):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_book('12355', my_book_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_book_should_read(my_book_repository, my_book_reader):
    my_book_repository.put(Ref.BookRomeoAndJuliet)

    view = await get_book('12355', my_book_reader)

    assert view.data.title == 'Romeo and Juliet'

# update_book
@pytest.mark.asyncio
async def test_update_book_should_fail_when_not_found(my_book_updater, my_payload_update):
    with pytest.raises(HTTPException) as exc:
        await update_book('1235465', my_payload_update, my_book_updater)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_book_should_fail_when_bad_request(my_book_repository, my_book_updater, my_payload_update):
    my_book_repository.put(Ref.BookRomeoAndJuliet)

    with pytest.raises(HTTPException) as exc:
        await update_book('1235465', my_payload_update, my_book_updater)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_update_book_should_fail_when_server_error(my_book_repository, my_book_updater, my_payload_update):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await update_book('1235465', my_payload_update, my_book_updater)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_update_book_should_run_when_update(
        my_book_repository,
        my_author_repository,
        my_editorial_repository,
        my_book_updater,
        my_payload_update
):
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_author_repository.put(Ref.AuthorShakespeare)
    my_editorial_repository.put(Ref.EditorialAnaya)

    await update_book('1235465', my_payload_update, my_book_updater)

    assert my_book_repository.stored is not None

# delete_book
@pytest.mark.asyncio
async def test_delete_book_should_fail_when_not_found(my_book_eraser):
    with pytest.raises(HTTPException) as exc:
        await delete_book('not-exists', my_book_eraser)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_book_should_fail_server_error(my_book_eraser, my_book_repository):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await delete_book('not-exists', my_book_eraser)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_delete_book_should_run_when_delete(my_book_eraser, my_book_repository):
    my_book_repository.put(Ref.BookRomeoAndJuliet)

    await delete_book('not-exists', my_book_eraser)

    assert my_book_repository.removed is not None

# book_available
@pytest.mark.asyncio
async def test_book_available_should_fail_when_not_found(my_book_available):
    payload = BookAvailableQueryPayload(sale=False)

    with pytest.raises(HTTPException) as exc:
        await book_available('not-exists', payload, my_book_available)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_book_available_should_fail_when_server_error(my_book_repository, my_book_available):
    my_book_repository.error('Database connection error')
    payload = BookAvailableQueryPayload(sale=False)

    with pytest.raises(HTTPException) as exc:
        await book_available('not-exists', payload, my_book_available)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_book_available_should_run(my_book_repository, my_book_available):
    book = my_book_repository.put(Ref.BookDonQuijote)
    book.change_stock(10)

    payload = BookAvailableQueryPayload(sale=False)

    result = await book_available('not-exists', payload, my_book_available)

    assert result.data.available is True
