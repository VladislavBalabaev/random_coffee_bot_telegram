from dataclasses import dataclass
from typing import Any

from nespresso.recsys.searchbase.document import DocAttribute
from nespresso.recsys.searchbase.index import INDEX_NAME, client

SCROLL_TIMEOUT = "30m"  # alive for 30 minutes


@dataclass
class SearchItem:
    nes_id: int
    score: float

    @classmethod
    def FromDict(cls, hit: dict[Any, Any]) -> "SearchItem":
        return cls(
            nes_id=int(hit["_id"]),
            score=float(hit["_score"]),
        )


@dataclass
class SearchResult:
    items: list[SearchItem] | None = None
    scroll_id: str | None = None
    expired: bool = False

    @classmethod
    def FromDict(cls, response: dict[Any, Any]) -> "SearchResult":
        hits = response["hits"]["hits"]

        items = [SearchItem.FromDict(hit) for hit in hits]
        scroll_id = response["_scroll_id"]

        return cls(items=items, scroll_id=scroll_id)


async def HybridSearch(text: str) -> SearchResult:
    attr = DocAttribute.FromText(text)

    search_body = {
        "size": 5,
        "_source": False,
        "query": {
            "bool": {  # composite query
                "should": [  # scores are summed
                    {"match": {"mynes_keywords": attr.keywords}},
                    {"knn": {"mynes_embedding": {"vector": attr.embedding, "k": 5}}},
                    {"match": {"cv_keywords": attr.keywords}},
                    {"knn": {"cv_embedding": {"vector": attr.embedding, "k": 5}}},
                ]
            }
        },
    }

    response = await client.search(
        index=INDEX_NAME,
        body=search_body,
        scroll=SCROLL_TIMEOUT,
    )

    return SearchResult.FromDict(response)


async def ScrollThroughResults(scroll_id: str) -> SearchResult:
    try:
        response = await client.scroll(
            scroll_id=scroll_id,
            scroll=SCROLL_TIMEOUT,  # refresh
        )
    except Exception:
        return SearchResult(expired=True)

    return SearchResult.FromDict(response)


async def FinishScrolling(scroll_id: str) -> None:
    await client.clear_scroll(scroll_id=scroll_id)
