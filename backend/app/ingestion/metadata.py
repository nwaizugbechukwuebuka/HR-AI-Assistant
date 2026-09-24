from dataclasses import asdict
from pathlib import Path

from backend.app.ingestion.chunker import TextChunk


def build_chunk_metadata(
    file_path: str | Path,
    chunks: list[TextChunk],
) -> list[dict]:
    """Build metadata records for vector-store chunks."""

    path = Path(file_path)

    records: list[dict] = []

    for chunk in chunks:
        record = asdict(chunk)

        record.update(
            {
                "filename": path.name,
                "source_path": str(path),
            }
        )

        records.append(record)

    return records