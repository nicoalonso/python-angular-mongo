from fastapi import Request

from src.domain.bus import DomainBus


def get_bus(request: Request) -> DomainBus:
    return request.app.state.bus


__all__ = [
    "get_bus",
]
