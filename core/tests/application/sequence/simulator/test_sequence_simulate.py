import pytest

from src.application.sequence.simulator.sequence_simulate import SequenceSimulate
from src.domain.sequence.exception import InvalidSequenceTypeError
from tests.doubles.infrastructure.persistence import SequenceNumberRepositoryStub


class TestSequenceSimulate:
    @pytest.fixture(autouse=True)
    def setup(self):
        repo_sequence = SequenceNumberRepositoryStub()
        self.simulator = SequenceSimulate(repo_sequence)

    @pytest.mark.asyncio
    async def test_dispatch_should_fail_when_invalid_type(self):
        with pytest.raises(InvalidSequenceTypeError):
            await self.simulator.dispatch('invalid-type')

    @pytest.mark.asyncio
    async def test_dispatch_should_run(self):
        result = await self.simulator.dispatch('sale')

        assert result.format() == 'F-00002'
