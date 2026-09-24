from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    """A searchable section of a source document."""

    text: str
    chunk_index: int


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[TextChunk]:
    """Split text into overlapping character-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )

    normalized_text = text.strip()

    if not normalized_text:
        return []

    chunks: list[TextChunk] = []

    start = 0
    chunk_index = 0
    step = chunk_size - overlap

    while start < len(normalized_text):
        end = min(
            start + chunk_size,
            len(normalized_text),
        )

        chunk = normalized_text[start:end].strip()

        if chunk:
            chunks.append(
                TextChunk(
                    text=chunk,
                    chunk_index=chunk_index,
                )
            )

        start += step
        chunk_index += 1

    return chunks