import logging

from nespresso.recsys.searchbase.client import client
from nespresso.recsys.searchbase.index import INDEX_NAME, DocAttr, DocSide


async def UpsertTextOpenSearch(
    nes_id: int,
    side: DocSide,
    text: str,
) -> None:
    attr = DocAttr.FromText(text)

    body = {
        "doc_as_upsert": True,
        "doc": {
            f"{side}_{DocAttr.Field.text}": attr.text,
            f"{side}_{DocAttr.Field.embedding}": attr.embedding,
        },
    }

    await client.update(
        index=INDEX_NAME,
        id=nes_id,
        body=body,
        refresh=True,  # immediately makes doc visible to search
    )

    logging.info(f"nes_id={nes_id} :: Document '{side}' side upserted successfully.")
