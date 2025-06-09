from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any

from aiogram import types
from cachetools import TTLCache

from nespresso.bot.lib.chat.username import GetChatTgUsername
from nespresso.db.models.tg_user import TgUser
from nespresso.db.services.user_context import user_ctx
from nespresso.recsys.searchbase.client import client
from nespresso.recsys.searchbase.index import INDEX_NAME, DocAttr, DocSide

_TIMEOUT = 60  # alive for 1 hour
_SCROLL_LIMIT = 1
_KNN_LIMIT = 30


@dataclass
class Profile:
    score: float
    nes_id: int
    name: str
    username: str
    phone_number: str
    email: str
    description: str

    @classmethod
    async def FromHit(cls, hit: dict[Any, Any]) -> Profile:
        nes_id = int(hit["_id"])

        ctx = await user_ctx()
        chat_id = await ctx.GetTgChatIdBy(nes_id)

        username = "[doesn't use this bot]"
        phone_number = "-/-"
        if chat_id:
            if tg := await GetChatTgUsername(chat_id):
                username = tg

            if tg := await ctx.GetTgUser(chat_id=chat_id, column=TgUser.phone_number):
                phone_number = tg

        name = "-/-"
        email = "-/-"
        if nes_user := await ctx.GetNesUser(nes_id=nes_id):
            name = nes_user.name or "-/-"
            email = nes_user.email_primary or "-/-"

        # TODO: add programm'year and format. For that need to see the data.

        return cls(
            score=float(hit["_score"]),
            nes_id=nes_id,
            name=name,
            username=username,
            phone_number=phone_number,
            email=email,
            description=str(
                hit["_source"][f"{DocSide.cv.value}_{DocAttr.Field.text.value}"]
            ),
        )


@dataclass
class Page:
    scroll_id: str
    number: int
    profile: Profile
    final_text: str | None = None

    @classmethod
    async def FromResponse(cls, response: dict[Any, Any], number: int) -> Page | None:
        hits = response["hits"]["hits"]
        assert len(hits) <= 1

        if not hits:
            return None

        return cls(
            scroll_id=response["_scroll_id"],
            number=number,
            profile=await Profile.FromHit(hits[0]),
        )

    def GetFormattedText(self) -> str:
        if self.final_text:
            return self.final_text

        self.final_text = ""
        self.final_text += f"[Page: {self.number}]\n\n"
        self.final_text += f"{self.profile.name}, "
        self.final_text += f"{self.profile.username}\n"
        self.final_text += f"phone: {self.profile.phone_number}\n"
        self.final_text += f"email: {self.profile.email}\n\n"
        self.final_text += f"{self.profile.description}"

        return self.final_text


class ScrollingSearch:
    def __init__(self) -> None:
        self.pages: list[Page] = []
        self.index: int = 0
        self.expired = False

    def _CreateBody(self, message: types.Message) -> dict[Any, Any]:
        if not message.text:
            raise ValueError("Expected message.text to be non-empty")

        attr = DocAttr.FromText(message.text)

        logging.info(f"chat_id={message.chat.id} :: Query text: '{attr.text}'")

        body = {
            "size": _SCROLL_LIMIT,
            "_source": True,
            "query": {
                "bool": {  # composite query
                    "should": [  # scores are summed
                        {
                            "match": {
                                f"{DocSide.mynes.value}_{DocAttr.Field.text.value}": attr.text,
                            }
                        },
                        {
                            "knn": {
                                f"{DocSide.mynes.value}_{DocAttr.Field.embedding.value}": {
                                    "vector": attr.embedding,
                                    "k": _KNN_LIMIT,
                                }
                            }
                        },
                        {
                            "match": {
                                f"{DocSide.cv.value}_{DocAttr.Field.text.value}": attr.text,
                            }
                        },
                        {
                            "knn": {
                                f"{DocSide.cv.value}_{DocAttr.Field.embedding.value}": {
                                    "vector": attr.embedding,
                                    "k": _KNN_LIMIT,
                                }
                            }
                        },
                    ]
                }
            },
        }

        return body

    def _CurrentPage(self) -> Page:
        return self.pages[self.index]

    async def HybridSearch(self, message: types.Message) -> Page | None:
        if self.pages:
            raise ValueError("HybridSearch() was called more than once.")

        body = self._CreateBody(message)

        response = await client.search(
            index=INDEX_NAME,
            body=body,
            scroll=f"{_TIMEOUT}m",
        )

        page = await Page.FromResponse(
            response=response,
            number=self.index,
        )
        if page:
            self.pages = [page]

        # TODO: check for score (if it is high enough) and output `None`

        return self._CurrentPage()

    def CanScrollFutherBackward(self) -> bool:
        return self.index > 0

    async def ScrollBackward(self) -> Page:
        if self.index == 0:
            raise ValueError("Can't scroll futher backward.")

        self.index -= 1

        return self._CurrentPage()

    def CanScrollFutherForward(self) -> bool:
        return self.index < self.pages[-1].number or not self.expired

    async def ScrollForward(self) -> Page | None:
        if not self.pages:
            raise ValueError("HybridSearch() must be called before scrolling forward.")

        if self.index < self.pages[-1].number:
            self.index += 1
            return self._CurrentPage()

        if self.expired:
            return None

        try:
            response = await client.scroll(
                scroll_id=self.pages[-1].scroll_id,
                scroll=f"{_TIMEOUT}m",  # refresh
            )
        except Exception:
            self.expired = True
            return None

        page = await Page.FromResponse(
            response=response,
            number=self.index + 1,
        )

        if not page:
            self.expired = True
            return None

        # TODO: check for score (if it is high enough) and output `None`

        self.pages.append(page)
        self.index += 1

        return self._CurrentPage()

    async def FinishScrolling(self) -> None:
        if not self.pages:
            raise ValueError(
                "HybridSearch() must be called before finishing scrolling."
            )

        await client.clear_scroll(scroll_id=self.pages[-1].scroll_id)


SEARCHES: TTLCache[uuid.UUID, ScrollingSearch] = TTLCache(
    maxsize=5000,
    ttl=_TIMEOUT * 60,
)
