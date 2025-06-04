import logging

from opensearchpy import AsyncHttpConnection, AsyncOpenSearch

from nespresso.core.configs.settings import settings
from nespresso.recsys.preprocessing.model import EMBEDDING_LEN

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
                "mynes_keywords": {
                    "type": "text",
                },
                "mynes_embedding": {
                    "type": "knn_vector",
                    "dimension": EMBEDDING_LEN,
                },
                "cv_keywords": {
                    "type": "text",
                },
                "cv_embedding": {
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
async def DeleteOpenSearchIndex() -> None:
    await client.indices.delete(index=INDEX_NAME)
