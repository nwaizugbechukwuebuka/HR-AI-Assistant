from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    """Shared document fields."""

    filename: str
    title: str
    file_path: str
    document_type: str


class DocumentCreate(DocumentBase):
    """Data required to create a document record."""

    pass


class DocumentResponse(DocumentBase):
    """Public document representation."""

    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )