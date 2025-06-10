import logging

from nespresso.recsys.searching.client import client
from nespresso.recsys.searching.index import INDEX_NAME, DocAttr, DocSide


async def UpsertTextOpenSearch(
    nes_id: int,
    side: DocSide,
    text: str,
) -> None:
    attr = DocAttr.FromText(text)

    body = {
        "doc_as_upsert": True,
        "doc": {
            f"{side.value}_{DocAttr.Field.text.value}": attr.text,
            f"{side.value}_{DocAttr.Field.embedding.value}": attr.embedding,
        },
    }

    await client.update(
        index=INDEX_NAME,
        id=nes_id,
        body=body,
        refresh=True,  # immediately makes doc visible to search
    )

    logging.info(
        f"nes_id={nes_id} :: Document '{side.value}' side upserted successfully."
    )
