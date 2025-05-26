import json

from sentence_transformers import SentenceTransformer

from nespresso.core.configs.paths import DIR_EMBEDDING_MODEL, PATH_EMBEDDING_DATA

MAX_TOKEN_LEN = 384

embedding_model = SentenceTransformer(model_name_or_path=str(DIR_EMBEDDING_MODEL))


def IsAllowedLen(text: str) -> bool:
    tokenized = embedding_model.tokenizer(text)

    return len(tokenized["input_ids"]) <= MAX_TOKEN_LEN


def CreateEmbedding(text: str) -> list[int]:
    embedding = embedding_model.encode(text, normalize_embeddings=True)

    return embedding.tolist()


def UpsertEmbedding(nes_id: int, embedding: list[int]) -> None:
    try:
        with open(PATH_EMBEDDING_DATA, "r", encoding="utf-8") as f:  # noqa: UP015
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

    with open(PATH_EMBEDDING_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
