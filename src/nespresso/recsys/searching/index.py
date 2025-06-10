import logging
from dataclasses import dataclass
from enum import Enum

from nespresso.recsys.searching.client import client
from nespresso.recsys.searching.preprocessing.embedding import CreateEmbedding
from nespresso.recsys.searching.preprocessing.model import EMBEDDING_LEN

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

    text_config = {"type": "text"}
    embedding_config = {"type": "knn_vector", "dimension": EMBEDDING_LEN}

    fields = [
        (DocSide.mynes, DocAttr.Field.text, text_config),
        (DocSide.mynes, DocAttr.Field.embedding, embedding_config),
        (DocSide.cv, DocAttr.Field.text, text_config),
        (DocSide.cv, DocAttr.Field.embedding, embedding_config),
    ]

    create_body = {
        "settings": {
            "index.knn": True,
        },
        "mappings": {
            "properties": {
                f"{side.value}_{field.value}": config for side, field, config in fields
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
    logging.info(f"# OpenSearch '{INDEX_NAME}' index deleted.")
