import json
from pathlib import Path

import faiss
import numpy as np


class VectorRetriever:
    """FAISS-backed semantic vector retriever."""

    def __init__(
        self,
        index_path: str | Path,
        metadata_path: str | Path,
    ) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        self.index = None
        self.metadata: list[dict] = []

    def build(
        self,
        embeddings,
        metadata: list[dict],
    ) -> None:
        """Build and store a FAISS index."""

        if len(metadata) == 0:
            raise ValueError("Metadata cannot be empty.")

        vectors = np.asarray(
            embeddings,
            dtype="float32",
        )

        if vectors.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2-dimensional array."
            )

        if vectors.shape[0] != len(metadata):
            raise ValueError(
                "Embedding count must match metadata count."
            )

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(dimension)
        index.add(vectors)

        self.index = index
        self.metadata = metadata

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            index,
            str(self.index_path),
        )

        self.metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(self) -> None:
        """Load an existing FAISS index and metadata."""

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {self.index_path}"
            )

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata file not found: {self.metadata_path}"
            )

        self.index = faiss.read_index(
            str(self.index_path)
        )

        self.metadata = json.loads(
            self.metadata_path.read_text(
                encoding="utf-8"
            )
        )

    def search(
        self,
        query_embedding,
        top_k: int = 5,
    ) -> list[dict]:
        """Return the most relevant document chunks."""

        if self.index is None:
            raise RuntimeError(
                "Vector index has not been loaded or built."
            )

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query = np.asarray(
            query_embedding,
            dtype="float32",
        )

        if query.ndim == 1:
            query = query.reshape(1, -1)

        scores, indices = self.index.search(
            query,
            min(top_k, self.index.ntotal),
        )

        results: list[dict] = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index < 0:
                continue

            result = dict(self.metadata[index])
            result["score"] = float(score)

            results.append(result)

        return results