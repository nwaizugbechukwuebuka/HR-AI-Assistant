from pathlib import Path

from backend.app.ai.embeddings import EmbeddingService
from backend.app.ai.retriever import VectorRetriever
from backend.app.ingestion.chunker import chunk_text
from backend.app.ingestion.document_loader import clean_text
from backend.app.ingestion.metadata import build_chunk_metadata
from backend.app.ingestion.text_extractor import extract_text_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
VECTOR_DIR = PROJECT_ROOT / "vector_store"

INDEX_PATH = VECTOR_DIR / "index.faiss"
METADATA_PATH = VECTOR_DIR / "metadata.json"


def ingest_documents() -> None:
    """Build the HR document vector index."""

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:
        raise RuntimeError(
            f"No PDF documents found in {DOCUMENTS_DIR}"
        )

    all_chunks = []
    all_metadata = []

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        raw_text = extract_text_from_pdf(
            pdf_file
        )

        cleaned_text = clean_text(
            raw_text
        )

        chunks = chunk_text(
            cleaned_text
        )

        metadata = build_chunk_metadata(
            pdf_file,
            chunks,
        )

        all_chunks.extend(chunks)
        all_metadata.extend(metadata)

        print(
            f"  Extracted characters: {len(cleaned_text)}"
        )
        print(
            f"  Chunks: {len(chunks)}"
        )

    texts = [
        chunk.text
        for chunk in all_chunks
    ]

    print(
        f"\nGenerating embeddings for {len(texts)} chunks..."
    )

    embedding_service = EmbeddingService()

    embeddings = embedding_service.encode(
        texts
    )

    retriever = VectorRetriever(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH,
    )

    retriever.build(
        embeddings=embeddings,
        metadata=all_metadata,
    )

    print("\nVector index created successfully.")
    print(f"Index: {INDEX_PATH}")
    print(f"Metadata: {METADATA_PATH}")


if __name__ == "__main__":
    ingest_documents()