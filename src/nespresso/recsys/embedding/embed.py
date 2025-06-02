from nespresso.recsys.embedding.model import (
    TOKEN_LEN,
    embedding_model,
)


def IsAllowedLen(text: str) -> bool:
    tokenized = embedding_model.tokenizer(text)

    return len(tokenized["input_ids"]) <= TOKEN_LEN


def CreateEmbedding(text: str) -> list[int]:
    embedding = embedding_model.encode(text, normalize_embeddings=True)

    return embedding.tolist()
