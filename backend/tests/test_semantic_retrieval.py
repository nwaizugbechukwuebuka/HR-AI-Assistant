from pathlib import Path

from backend.app.ai.embeddings import EmbeddingService
from backend.app.ai.retriever import VectorRetriever


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INDEX_PATH = PROJECT_ROOT / "vector_store" / "index.faiss"
METADATA_PATH = PROJECT_ROOT / "vector_store" / "metadata.json"


QUERIES = [
    "What are the rules employees must follow when using company resources?",
    "What benefits are available to employees?",
    "What should a new employee do during onboarding?",
    "How many days of leave can an employee take?",
    "What are the expectations for employee conduct?",
    "Can employees work remotely and under what conditions?",
]


def test_semantic_retrieval_against_hr_documents() -> None:
    """Verify semantic retrieval against the indexed HR knowledge base."""

    assert INDEX_PATH.exists(), (
        f"FAISS index not found: {INDEX_PATH}. "
        "Run the document ingestion pipeline first."
    )

    assert METADATA_PATH.exists(), (
        f"Metadata file not found: {METADATA_PATH}. "
        "Run the document ingestion pipeline first."
    )

    embedding_service = EmbeddingService()

    retriever = VectorRetriever(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH,
    )

    retriever.load()

    assert retriever.index is not None
    assert retriever.index.ntotal > 0
    assert len(retriever.metadata) == retriever.index.ntotal

    print("\n=== HR DOCUMENT SEMANTIC RETRIEVAL TEST ===")

    for query in QUERIES:
        query_embedding = embedding_service.encode([query])

        results = retriever.search(
            query_embedding=query_embedding,
            top_k=3,
        )

        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        assert results, (
            f"No retrieval results returned for query: {query}"
        )

        for rank, result in enumerate(results, start=1):
            print(f"\n[{rank}]")
            print(f"Score: {result['score']:.4f}")
            print(f"Document: {result['filename']}")
            print(f"Chunk: {result['chunk_index']}")
            print(f"Text: {result['text'][:500]}")

        print()

    print("\nSemantic retrieval test completed successfully.")