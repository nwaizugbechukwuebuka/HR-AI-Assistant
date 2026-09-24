import re


def clean_text(text: str) -> str:
    """Normalize extracted document text."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize repeated whitespace while preserving paragraphs.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces surrounding line breaks.
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()