from typing import Annotated

from fastapi import Depends, HTTPException

from src.application.sequence.simulator import SequenceSimulate
from src.domain.sequence.exception import InvalidSequenceTypeError
from src.infrastructure.dependencies.sequence import get_sequence_simulate
from src.infrastructure.router import router
from src.presentation.v1.sequence import SequenceReadView


@router.get("/sequences/{type}/simulate", tags=["Sequences"], summary='Simulates a sequence')
async def simulate_sequence(
        type: str,
        simulator: Annotated[SequenceSimulate, Depends(get_sequence_simulate)]
) -> SequenceReadView:
    """Simulates a sequence number for the given type."""
    try:
        sequence_number = await simulator.dispatch(type)
        return SequenceReadView(sequence_number)
    except InvalidSequenceTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


__all__ = [
    "simulate_sequence",
]
