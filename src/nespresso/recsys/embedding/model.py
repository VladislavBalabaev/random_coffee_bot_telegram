from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

from nespresso.core.configs.paths import DIR_EMBEDDING_MODEL


def EnsureEmbeddingModel() -> None:
    snapshot_download(
        repo_id="sentence-transformers/all-mpnet-base-v2",
        local_dir=DIR_EMBEDDING_MODEL,
    )


embedding_model = SentenceTransformer(model_name_or_path=str(DIR_EMBEDDING_MODEL))
