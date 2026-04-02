from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from src.infrastructure.bus import InMemoryDomainBus
from src.infrastructure.messenger import InMemoryMessenger
from src.infrastructure.messenger.adapter import RabbitMQMessenger
from src.infrastructure.persistence.pymongo import MongoConnection
from src.infrastructure.router import router
# noinspection PyUnresolvedReferences
from src.infrastructure.controller import *
from config import Settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    settings = Settings()
    application.state.settings = settings

    bus = InMemoryDomainBus()
    adapter = RabbitMQMessenger(
        dsn=settings.rabbitmq_dsn,
        exchange=settings.rabbitmq_exchange,
        queue=settings.rabbitmq_queue,
    )
    InMemoryMessenger(adapter, bus)
    application.state.bus = bus

    mongo = MongoConnection(uri=settings.database_url, db_name=settings.database_name)
    await mongo.connect()
    application.state.mongo = mongo
    try:
        yield
    finally:
        await mongo.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect to API documentation
@app.get("/v1/doc", include_in_schema=False)
def api_docs():
    return RedirectResponse(url="/docs")


app.include_router(router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.detail, "code": exc.status_code}),
    )
