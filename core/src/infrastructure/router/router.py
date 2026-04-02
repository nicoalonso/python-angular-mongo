from fastapi import APIRouter
from fastapi.params import Depends

from src.infrastructure.dependencies.handlers_register import handlers_register

router = APIRouter(prefix="/library/v1", dependencies=[Depends(handlers_register)])
