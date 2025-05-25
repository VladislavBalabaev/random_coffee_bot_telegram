import json

from nespresso.core.configs.paths import PATH_EMBEDDING


def UpsertEmbeddings(nes_id: int, embedding: list[int]) -> None:
    try:
        with open(PATH_EMBEDDING, "r", encoding="utf-8") as f:  # noqa: UP015
            data = json.load(f)
    except FileNotFoundError:
        data = []

    found = False
    for item in data:
        if item["nes_id"] == nes_id:
            item["embedding"] = embedding
            found = True
            break

    if not found:
        data.append({"nes_id": nes_id, "embedding": embedding})

    with open(PATH_EMBEDDING, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
