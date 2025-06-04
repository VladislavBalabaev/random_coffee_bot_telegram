import logging
from dataclasses import dataclass
from enum import Enum

from nespresso.recsys.preprocessing.embedding import CreateEmbedding
from nespresso.recsys.preprocessing.keywords import ExtractKeywords
from nespresso.recsys.searchbase.index import INDEX_NAME, client


class DocPart(Enum):
    mynes = "mynes"
    cv = "cv"


@dataclass
class DocAttribute:
    keywords: str
    embedding: list[float]

    @classmethod
    def FromText(cls, text: str) -> "DocAttribute":
        return DocAttribute(
            keywords=ExtractKeywords(text),
            embedding=CreateEmbedding(text),
        )


async def UpsertDocAttribute(
    nes_id: int,
    part: DocPart,
    attribute: DocAttribute,
) -> None:
    body = {
        "doc_as_upsert": True,
        f"{part.name}_keywords": attribute.keywords,
        f"{part.name}_embedding": attribute.embedding,
    }

    await client.update(
        index=INDEX_NAME,
        id=nes_id,
        body=body,
        refresh=True,  # immediately makes doc visible to search
    )

    logging.info(
        f"Document - part '{part.name}' of nes_id='{nes_id}' upserted successfully."
    )
