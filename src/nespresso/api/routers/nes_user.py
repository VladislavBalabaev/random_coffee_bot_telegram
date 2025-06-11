import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from nespresso.core.configs.settings import settings
from nespresso.db.models.nes_user import NesUser
from nespresso.db.schemas.nes_user import NesUserIn, NesUserOut
from nespresso.db.services.user_context import GetUserContextService

router = APIRouter()

_MYNES_TOKEN = settings.MYNES_TOKEN.get_secret_value()


TokenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials, check the token in the `authorization_token` header",
    # headers={"WWW-Authenticate": "Bearer"},
)

# oauth2 = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="authorization_token", auto_error=False)


def VerifyMyNesToken(token: Annotated[str, Depends(api_key_header)]) -> None:
    if token != _MYNES_TOKEN:
        logging.warning(f"Invalid token verification attempt:\ntoken='{token}'")
        raise TokenException


def NesUserPydanticToSQLAlchemy(instance: NesUserIn) -> NesUser:
    raw = instance.model_dump(mode="json", exclude_unset=True)
    return NesUser(**raw)


@router.post(
    "/upsert_nes_info/",
    status_code=status.HTTP_201_CREATED,
    summary="Create or update NES user",
    description="To upsert information about NES user pass body with it's full info even with NULLs.\n\n**Authentication**: You must provide the token in the `authorization_token` header.\n",
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
    ctx = await GetUserContextService()

    alchemy_nes_user: NesUser = NesUserPydanticToSQLAlchemy(nes_user)

    await ctx.UpsertNesUser(alchemy_nes_user)

    return nes_user
