from nespresso.recsys.preprocessing.model import model


def CalculateTokenLen(text: str) -> int:
    tokenized = model.tokenizer(text)

    return len(tokenized["input_ids"])


def CreateEmbedding(text: str) -> list[float]:
    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()
