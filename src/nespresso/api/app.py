import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from nespresso.api.routers import nes_user
from nespresso.core.logs import LoggerShutdown, LoggerStart


class Tags(Enum):
    users = "users"
    analytics = "analytics"


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def RequestValidationErrorHandler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logging.error(f"Validation error on {request.method} {request.url}: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@asynccontextmanager
async def Lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await LoggerStart()
    yield
    await LoggerShutdown()


app = FastAPI(lifespan=Lifespan)

app.include_router(nes_user.router, prefix="/user", tags=[Tags.users])
