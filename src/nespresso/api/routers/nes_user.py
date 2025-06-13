import logging
from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from nespresso.core.configs.settings import settings
from nespresso.db.models.nes_user import NesUser
from nespresso.db.models.schemas.nes_user import NesUserIn, NesUserOut
from nespresso.db.services.user_context import GetUserContextService
from nespresso.recsys.searching.document import UpsertTextOpenSearch
from nespresso.recsys.searching.index import DocSide

router = APIRouter()

_MYNES_TOKEN = settings.MYNES_TOKEN.get_secret_value()


def NesUserPydanticToSQLAlchemy(instance: NesUserIn) -> NesUser:
    raw = instance.model_dump(mode="json", exclude_unset=True)
    return NesUser(**raw)


def _FormatScalarFields(user: NesUserIn) -> list[str]:
    labels = {
        "Name": user.name,
        "City": user.city,
        "Region": user.region,
        "Country": user.country,
        "Program": user.program,
        "Class": user.class_name,
    }

    return [f"{label} – {val}" for label, val in labels.items() if val]


def _FormatListFields(user: NesUserIn) -> list[str]:
    labels = {
        "Hobbies": user.hobbies,
        "Industry expertise": user.industry_expertise,
        "Country expertise": user.country_expertise,
        "Professional expertise": user.professional_expertise,
    }

    return [f"{label} – {', '.join(vals)}" for label, vals in labels.items() if vals]


def _FormatModelSection(
    label: str,
    models: BaseModel | Sequence[BaseModel] | None,
) -> str | None:
    if not models:
        return None

    if isinstance(models, BaseModel):
        items: Sequence[BaseModel] = [models]
    else:
        items = models

    entries: list[str] = []
    for m in items:
        data = m.model_dump()
        parts = [f"{k} – {v}" for k, v in data.items() if v is not None]

        if parts:
            entries.append(", ".join(parts))

    if not entries:
        return None

    sub = "\n".join(f"  – {e}" for e in entries)
    return f"{label}:\n{sub}"


def GetNesUserModelText(nes_user: NesUserIn) -> str:
    sections: list[str] = []
    sections += _FormatScalarFields(nes_user)
    sections += _FormatListFields(nes_user)

    main_work = _FormatModelSection("Main work", nes_user.main_work)
    if main_work:
        sections.append(main_work)

    for label, attr in [
        ("Additional work", nes_user.additional_work),
        ("Pre-NES education", nes_user.pre_nes_education),
        ("Post-NES education", nes_user.post_nes_education),
    ]:
        section = _FormatModelSection(label, attr)
        if section:
            sections.append(section)

    return ".\n".join(sections)


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


@router.post(
    path="/upsert_nes_info/",
    status_code=status.HTTP_201_CREATED,
    summary="Create or update NES user.",
    description="To upsert info about NES user pass body with it's full info even with NULLs.\n\n"
    "**Authentication**: You must provide the token in the `authorization_token` header.",
    response_description="`nes_id` of NES user upserted.",
)
async def UpsertNesUser(
    nes_user: Annotated[
        NesUserIn,
        Body(
            title="NesUser info.",
            description="Request body containing NesUser info.",
        ),
    ],
    token: Annotated[str, Depends(VerifyMyNesToken)],
) -> NesUserOut:
    ctx = await GetUserContextService()

    alchemy_nes_user: NesUser = NesUserPydanticToSQLAlchemy(nes_user)
    await ctx.UpsertNesUser(alchemy_nes_user)

    text = GetNesUserModelText(nes_user)
    await UpsertTextOpenSearch(
        nes_id=nes_user.nes_id,
        side=DocSide.mynes,
        text=text,
    )

    return nes_user
