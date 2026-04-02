from src.domain.sequence import SequenceNumberRepository, SequenceNumber, SequenceType
from src.domain.sequence.exception import InvalidSequenceTypeError


class SequenceSimulate:
    """
    Use case for simulating a sequence number
    """
    def __init__(self, repo_sequence_number: SequenceNumberRepository):
        self.repo_sequence_number = repo_sequence_number

    async def dispatch(self, type_: str) -> SequenceNumber:
        """
        Simulate a sequence number for the given type.

        :param type_: The type of sequence to simulate.
        :return: The simulated sequence number as a string.
        """
        sequence_type = SequenceType.try_from(type_)
        if not sequence_type:
            raise InvalidSequenceTypeError()

        return await self.repo_sequence_number.obtain_by_type(sequence_type)
