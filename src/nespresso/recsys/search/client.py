import logging
from dataclasses import dataclass
from typing import Any

from opensearchpy import AsyncHttpConnection, AsyncOpenSearch

from nespresso.core.configs.env_reader import settings
from nespresso.recsys.embedding.model import EMBEDDING_LEN

INDEX_NAME = "nes_users"
SCROLL_TIMEOUT = "30m"  # scroll alive for 30 minutes

client = AsyncOpenSearch(
    hosts=[
        {
            "host": "nespresso_opensearch",
            "port": 9200,
            "scheme": "http",
        }
    ],
    http_auth=("admin", settings.OPENSEARCH_INITIAL_ADMIN_PASSWORD.get_secret_value()),
    connection_class=AsyncHttpConnection,
    use_ssl=False,
    verify_certs=False,
)


async def EnsureOpenSearchIndex() -> None:
    if await client.indices.exists(index=INDEX_NAME):
        await client.indices.clear_cache(index=INDEX_NAME, query=True)
        return

    create_body = {
        "settings": {
            "index.knn": True,
        },
        "mappings": {
            "properties": {
                "user_text": {
                    "type": "text",
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": EMBEDDING_LEN,
                },
            }
        },
    }

    await client.indices.create(
        index=INDEX_NAME,
        body=create_body,
    )

    logging.info(f"# OpenSearch '{INDEX_NAME}' index created.")


# TODO: remove this later
# async def DeleteIndex() -> None:
#     await client.indices.delete(index=INDEX_NAME)


async def UpsertDocument(
    nes_id: int,
    user_text: str,
    embedding: list[float],
) -> None:
    doc = {
        "user_text": user_text,
        "embedding": embedding,
    }

    await client.index(
        index=INDEX_NAME,
        id=nes_id,
        body=doc,
        refresh=True,  # immediately makes doc visible to search
    )

    logging.info(f"Document of nes_id='{nes_id}' is upserted successfully.")


@dataclass
class SearchItem:
    nes_id: int
    score: float
    source_user_text: str

    @classmethod
    def FromDict(cls, hit: dict[Any, Any]) -> "SearchItem":
        return cls(
            nes_id=int(hit["_id"]),
            score=float(hit["_score"]),
            source_user_text=str(hit["_source"]["user_text"]),
        )


@dataclass
class SearchResult:
    items: list[SearchItem] | None = None
    scroll_id: str | None = None
    expired: bool = False

    @classmethod
    def FromDict(cls, response: dict[Any, Any]) -> "SearchResult":
        items = [SearchItem.FromDict(hit) for hit in response["hits"]["hits"]]
        scroll_id = response["_scroll_id"]

        return cls(items=items, scroll_id=scroll_id)


async def HybridSearch(
    user_text: str,
    embedding: list[int],
) -> SearchResult:
    search_body = {
        "size": 5,
        "query": {
            "bool": {  # composite query type
                "should": [  # scores from individual queries are summed
                    {
                        "match": {
                            # If the document has at least one token that matches → it’s selected as a match.
                            # Then **BM25** algorithm is used to calculate a relevance score for that document.
                            "user_text": user_text,  # make keyword extraction before (becuase we have "chatty" user experience)
                        }
                    },
                    {
                        "knn": {
                            "embedding": {
                                "vector": embedding,
                                "k": 5,
                            }
                        }
                    },
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
