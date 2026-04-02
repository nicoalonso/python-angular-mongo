from fastapi import Depends

from src.application.sequence.simulator import SequenceSimulate
from src.infrastructure.dependencies.repository import get_sequence_number_repository


def get_sequence_simulate(repo_sequence_number=Depends(get_sequence_number_repository)) -> SequenceSimulate:
    return SequenceSimulate(repo_sequence_number)


__all__ = [
    "get_sequence_simulate",
]
