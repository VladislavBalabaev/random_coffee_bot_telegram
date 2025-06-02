from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

from nespresso.core.configs.paths import DIR_EMBEDDING

TOKEN_LEN = 384
EMBEDDING_LEN = 768

_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"


def EnsureEmbeddingModel() -> None:
    snapshot_download(
        repo_id=_MODEL_NAME,
        local_dir=DIR_EMBEDDING,
    )


def LoadEmbeddingModel() -> SentenceTransformer:
    EnsureEmbeddingModel()

    return SentenceTransformer(model_name_or_path=str(DIR_EMBEDDING))


embedding_model = LoadEmbeddingModel()
