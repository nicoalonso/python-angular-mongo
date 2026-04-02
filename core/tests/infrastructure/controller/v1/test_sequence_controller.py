import pytest
from fastapi import HTTPException

from src.application.sequence.simulator import SequenceSimulate
from src.infrastructure.controller.v1.sequence_controller import simulate_sequence
from tests.doubles.infrastructure.persistence import SequenceNumberRepositoryStub


@pytest.fixture()
def my_sequence_repository():
    return SequenceNumberRepositoryStub()

@pytest.fixture()
def my_simulator(my_sequence_repository):
    return SequenceSimulate(my_sequence_repository)


# simulate_sequence
@pytest.mark.asyncio
async def test_simulate_sequence_should_fail_when_bad_request(my_simulator):
    with pytest.raises(HTTPException) as exc:
        await simulate_sequence('wrong', my_simulator)

    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_simulate_sequence_should_fail_when_server_error(my_simulator, my_sequence_repository):
    my_sequence_repository.error('Database connection error')

    with pytest.raises(HTTPException) as exc:
        await simulate_sequence('sale', my_simulator)

    assert exc.value.status_code == 500

@pytest.mark.asyncio
async def test_simulate_sequence_should_read(my_simulator):
    view = await simulate_sequence('sale', my_simulator)

    assert view.data.number == 'F-00002'
