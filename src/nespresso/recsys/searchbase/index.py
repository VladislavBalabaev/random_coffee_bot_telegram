import logging
from dataclasses import dataclass
from enum import Enum

from nespresso.recsys.preprocessing.embedding import CreateEmbedding
from nespresso.recsys.preprocessing.model import EMBEDDING_LEN
from nespresso.recsys.searchbase.client import client

INDEX_NAME = "nes_users"


class DocSide(str, Enum):
    mynes = "mynes"
    cv = "cv"


@dataclass
class DocAttr:
    text: str
    embedding: list[float]

    class Field(str, Enum):
        text = "text"
        embedding = "embedding"

    @classmethod
    def FromText(cls, text: str) -> "DocAttr":
        return cls(
            text=text,
            embedding=CreateEmbedding(text),
        )


async def EnsureOpenSearchIndex() -> None:
    if await client.indices.exists(index=INDEX_NAME):
        await client.indices.clear_cache(index=INDEX_NAME, query=True)
        return

    text_settings = {"type": "text"}
    embedding_settings = {"type": "knn_vector", "dimension": EMBEDDING_LEN}

    fields = [
        (DocSide.mynes, DocAttr.Field.text, text_settings),
        (DocSide.mynes, DocAttr.Field.embedding, embedding_settings),
        (DocSide.cv, DocAttr.Field.text, text_settings),
        (DocSide.cv, DocAttr.Field.embedding, embedding_settings),
    ]

    create_body = {
        "settings": {
            "index.knn": True,
        },
        "mappings": {
            "properties": {f"{side}_{field}": config for side, field, config in fields}
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
    logging.info(f"# OpenSearch '{INDEX_NAME}' index deleted.")
