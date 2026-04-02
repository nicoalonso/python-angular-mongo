import pytest
from fastapi import HTTPException

from src.application.borrow.checkin import BorrowCheckinPayload, BorrowCheckin
from src.application.borrow.creator import BorrowCreate, BorrowCreatePayload
from src.application.borrow.list import BorrowList, BorrowQueryPayload
from src.application.borrow.reader import BorrowRead
from src.infrastructure.controller import *
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
def my_borrow_repository(my_customer_repository):
    return BorrowRepositoryStub(repo_customer=my_customer_repository)

@pytest.fixture()
def my_borrow_line_repository(my_borrow_repository, my_book_repository):
    return BorrowLineRepositoryStub(
        repo_borrow=my_borrow_repository,
        repo_book=my_book_repository,
    )

@pytest.fixture()
def my_borrow_lister(my_borrow_repository):
    return BorrowList(my_borrow_repository)

@pytest.fixture()
def my_borrow_creator(
        my_borrow_repository,
        my_borrow_line_repository,
        my_customer_repository,
        my_book_repository,
):
    repo_sequence_number = SequenceNumberRepositoryStub()
    repo_user = UserRepositoryStub()
    return BorrowCreate(
        my_borrow_repository,
        my_borrow_line_repository,
        my_customer_repository,
        my_book_repository,
        repo_sequence_number,
        repo_user,
    )

@pytest.fixture()
def my_payload_create(my_loader):
    data = my_loader.load('borrow-create')
    return BorrowCreatePayload(**data)

@pytest.fixture()
def my_borrow_reader(my_borrow_repository, my_borrow_line_repository):
    return BorrowRead(my_borrow_repository, my_borrow_line_repository)

@pytest.fixture()
def my_borrow_checker(
        my_borrow_repository,
        my_borrow_line_repository
):
    repo_user = UserRepositoryStub()
    return BorrowCheckin(
        my_borrow_repository,
        my_borrow_line_repository,
        repo_user,
    )

@pytest.fixture()
def my_payload_checkin(my_loader):
    data = my_loader.load('borrow-checkin')
    return BorrowCheckinPayload(**data)


# get_borrows
@pytest.mark.asyncio
async def test_get_borrows_should_fail_when_wrong_field(my_borrow_lister):
    query = BorrowQueryPayload(sort='-wrong')
    with pytest.raises(HTTPException) as exc:
        await get_borrows(query, my_borrow_lister)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_borrows_should_fail_when_server_error(my_borrow_repository, my_borrow_lister):
    my_borrow_repository.error('Database connection error')
    query = BorrowQueryPayload()

    with pytest.raises(HTTPException) as exc:
        await get_borrows(query, my_borrow_lister)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_borrows_should_run(my_borrow_repository, my_borrow_lister):
    my_borrow_repository.attach_all()
    query = BorrowQueryPayload()

    result = await get_borrows(query, my_borrow_lister)

    assert len(result.items) > 0

# create_borrow
@pytest.mark.asyncio
async def test_create_borrow_should_fail_when_book_not_found(my_borrow_creator, my_payload_create):
    with pytest.raises(HTTPException) as exc:
        await create_borrow(my_payload_create, my_borrow_creator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_create_borrow_should_fail_when_server_error(my_book_repository, my_borrow_creator, my_payload_create):
    my_book_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await create_borrow(my_payload_create, my_borrow_creator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_create_borrow_should_run_when_create(
        my_borrow_repository,
        my_book_repository,
        my_customer_repository,
        my_borrow_creator,
        my_payload_create
):
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_customer_repository.put(Ref.CustomerJohnDoe)

    await create_borrow(my_payload_create, my_borrow_creator)

    assert my_borrow_repository.stored is not None

# get_borrow
@pytest.mark.asyncio
async def test_get_borrow_should_fail_when_not_found(my_borrow_reader):
    with pytest.raises(HTTPException) as exc:
        await get_borrow('not-exists', my_borrow_reader)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_borrow_should_fail_when_server_error(my_borrow_repository, my_borrow_reader):
    my_borrow_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await get_borrow('12355', my_borrow_reader)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_get_borrow_should_read(
        my_borrow_repository,
        my_borrow_line_repository,
        my_borrow_reader,
):
    my_borrow_repository.put(Ref.BorrowJohnDoe)
    my_borrow_line_repository.attach(Ref.BorrowLineJohnRomeoAndJuliet)

    view = await get_borrow('12355', my_borrow_reader)

    assert len(view.data.lines) == 1

# checkin_borrow
@pytest.mark.asyncio
async def test_checkin_borrow_should_fail_when_not_found(my_borrow_checker, my_payload_checkin):
    with pytest.raises(HTTPException) as exc:
        await checkin_borrow('1235465', my_payload_checkin, my_borrow_checker)

    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_checkin_borrow_should_fail_when_server_error(my_borrow_repository, my_borrow_checker, my_payload_checkin):
    my_borrow_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await checkin_borrow('1235465', my_payload_checkin, my_borrow_checker)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_checkin_borrow_should_run_when_update(
        my_borrow_repository,
        my_borrow_line_repository,
        my_book_repository,
        my_borrow_checker,
        my_payload_checkin
):
    my_borrow_repository.put(Ref.BorrowJohnDoe)
    my_book_repository.put(Ref.BookRomeoAndJuliet)
    my_borrow_line_repository.attach(Ref.BorrowLineJohnRomeoAndJuliet)

    await checkin_borrow('1235465', my_payload_checkin, my_borrow_checker)

    assert my_borrow_repository.stored is not None
