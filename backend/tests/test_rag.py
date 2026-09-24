from backend.app.ingestion.chunker import chunk_text
from backend.app.ingestion.document_loader import clean_text


def test_clean_text_removes_excessive_whitespace() -> None:
    """Verify document text normalization."""

    text = "Hello   world.\n\n\n\nNext section."

    cleaned = clean_text(text)

    assert cleaned == "Hello world.\n\nNext section."


def test_chunk_text_creates_chunks() -> None:
    """Verify deterministic text chunking."""

    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) == 3
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[2].chunk_index == 2


def test_chunk_text_empty_input() -> None:
    """Verify empty documents produce no chunks."""

    assert chunk_text("") == []


def test_chunk_text_rejects_invalid_overlap() -> None:
    """Verify invalid chunk configuration is rejected."""

    try:
        chunk_text(
            "Some text",
            chunk_size=100,
            overlap=100,
        )
    except ValueError as exc:
        assert "smaller than chunk_size" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError was not raised."
        )