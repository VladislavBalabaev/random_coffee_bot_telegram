import logging
from dataclasses import dataclass
from typing import Any

from aiogram import types

from nespresso.recsys.searchbase.document import DocAttribute
from nespresso.recsys.searchbase.index import INDEX_NAME, client

_TIMEOUT = "30m"  # alive for 30 minutes
_ITEMS = 5


@dataclass
class SearchItem:
    nes_id: int
    score: float

    @classmethod
    def FromHit(cls, hit: dict[Any, Any]) -> "SearchItem":
        return cls(
            nes_id=int(hit["_id"]),
            score=float(hit["_score"]),
        )


@dataclass
class SearchPage:
    number: int
    items: list[SearchItem]
    scroll_id: str

    @staticmethod
    def _ExtractItems(response: dict[Any, Any]) -> list[SearchItem]:
        return [SearchItem.FromHit(hit) for hit in response["hits"]["hits"]]

    @classmethod
    def FromResponse(cls, response: dict[Any, Any], number: int) -> "SearchPage":
        return cls(
            number=number,
            items=SearchPage._ExtractItems(response),
            scroll_id=response["_scroll_id"],
        )


class ScrollingSearch:
    def __init__(self) -> None:
        self.pages: list[SearchPage] = []
        self.index: int = 0
        self.expired = False

    def _CreateBody(self, message: types.Message) -> dict[Any, Any]:
        if not message.text:
            raise ValueError("Expected message.text to be non-empty")

        attr = DocAttribute.FromText(message.text)

        logging.info(f"chat_id={message.chat.id} :: Query keywords: '{attr.keywords}'")

        body = {
            "size": _ITEMS,
            "_source": False,
            "query": {
                "bool": {  # composite query
                    "should": [  # scores are summed
                        {"match": {"mynes_keywords": attr.keywords}},
                        {
                            "knn": {
                                "mynes_embedding": {
                                    "vector": attr.embedding,
                                    "k": _ITEMS,
                                }
                            }
                        },
                        {"match": {"cv_keywords": attr.keywords}},
                        {
                            "knn": {
                                "cv_embedding": {
                                    "vector": attr.embedding,
                                    "k": _ITEMS,
                                }
                            }
                        },
                    ]
                }
            },
        }

        return body

    def _CurrentPage(self) -> SearchPage:
        return self.pages[self.index]

    async def HybridSearch(self, message: types.Message) -> SearchPage | None:
        if self.pages:
            raise ValueError("HybridSearch() was called more than once.")

        body = self._CreateBody(message)

        response = await client.search(
            index=INDEX_NAME,
            body=body,
            scroll=_TIMEOUT,
        )

        page = SearchPage.FromResponse(
            response=response,
            number=self.index,
        )
        self.pages = [page]

        # TODO: check for score (if it is high enough) and output `None`

        return self._CurrentPage()

    async def ScrollBackward(self) -> SearchPage | None:
        if self.index == 0:
            return None

        self.index -= 1

        return self._CurrentPage()

    async def ScrollForward(self) -> SearchPage | None:
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
                scroll=_TIMEOUT,  # refresh
            )
        except Exception:
            self.expired = True
            return None

        page = SearchPage.FromResponse(
            response=response,
            number=self.index + 1,
        )

        if not page.items:
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
