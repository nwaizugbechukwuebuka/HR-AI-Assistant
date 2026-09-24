from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """Generate vector embeddings for document and query text."""

    def __init__(
        self,
        model_name: str = MODEL_NAME,
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def encode(
        self,
        texts: list[str],
    ):
        """Encode multiple text strings into vectors."""

        if not texts:
            return []

        return self.model.encode(
            texts,
            normalize_embeddings=True,
        )