import logging
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from nespresso.core.configs.env_reader import settings
from nespresso.core.services import user_ctx
from nespresso.db.models.nes_user import NesUser
from nespresso.schemas.nes_user import NesUserIn, NesUserOut

router = APIRouter()

_MYNES_TOKEN = settings.MYNES_TOKEN.get_secret_value()


class Tags(Enum):
    users = "users"
    analytics = "analytics"


TokenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def VerifyMyNesToken(token: Annotated[str, Depends(oauth2)]) -> None:
    if token != _MYNES_TOKEN:
        logging.warning(f"Invalid token verification attempt:\ntoken='{token}'")
        raise TokenException


def NesUserPydanticToSQLAlchemy(instance: NesUserIn) -> NesUser:
    raw = instance.model_dump(mode="json", exclude_unset=True)
    return NesUser(**raw)


@router.post(
    "/user/data/",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.users],
    summary="Create or update NES user",
    description="To upsert information about NES user pass body with it's full info even with NULLs.",
    response_description="`nes_id` of NES user upserted.",
)
async def UpsertNesUser(
    nes_user: Annotated[
        NesUserIn,
        Body(
            title="NesUser information",
            description="Request body containing NesUser information",
        ),
    ],
    token: Annotated[str, Depends(VerifyMyNesToken)],
) -> NesUserOut:
    ctx = await user_ctx()

    alchemy_nes_user: NesUser = NesUserPydanticToSQLAlchemy(nes_user)

    await ctx.UpsertNesUser(alchemy_nes_user)

    return nes_user
