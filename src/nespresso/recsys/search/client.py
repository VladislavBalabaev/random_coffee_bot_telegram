import logging

from opensearchpy import AsyncOpenSearch

from nespresso.core.configs.env_reader import settings
from nespresso.recsys.embedding.embed import MAX_TOKEN_LEN

INDEX_NAME = "nes_users"

client = AsyncOpenSearch(
    hosts=[
        {
            "host": "nespresso_opensearch",
            "port": 9200,
            "scheme": "http",
        }
    ],
    http_auth=("admin", settings.OPENSEARCH_INITIAL_ADMIN_PASSWORD.get_secret_value()),
    use_ssl=False,
    verify_certs=False,
)


async def EnsureOpenSearchIndex() -> None:
    logging.info("\n\n# hmm.\n")

    exists = await client.indices.exists(index=INDEX_NAME)

    if exists:
        return

    index_settings = {
        "mappings": {
            "properties": {
                "user_text": {
                    "type": "text",
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": MAX_TOKEN_LEN,
                },
            }
        }
    }

    await client.indices.create(
        index=INDEX_NAME,
        body=index_settings,
    )

    logging.info(f"# OpenSearch '{INDEX_NAME}' index created.")


# async def DeleteIndex() -> None:
#     await client.indices.delete(index=INDEX_NAME)


async def AddDocumentToIndex() -> None:
    doc = {
        "user_text": "Hello world",
        "embedding": [0.1, 0.2, 0.3, ...],
    }
    await client.index(index="users", id="user_1", body=doc, refresh=True)


async def HybridSearch(user_text: str, embedding: list[int]) -> None:
    response = await client.search(  # noqa: F841
        index=INDEX_NAME,
        body={
            "size": 5,  # size???
            "query": {
                "bool": {  # multi_match???
                    "must": [  # must??? how about mean-pooling???
                        {
                            "match": {
                                "user_text": user_text,
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
        },
    )

    # print(response)
