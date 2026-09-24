from sqlalchemy.orm import Session

from backend.app.db.models import Document
from backend.app.db.repositories import create_document
from backend.app.schemas.document import DocumentCreate


def register_document(
    db: Session,
    document_data: DocumentCreate,
) -> Document:
    """Register an HR document in the database."""

    return create_document(
        db=db,
        filename=document_data.filename,
        title=document_data.title,
        file_path=document_data.file_path,
        document_type=document_data.document_type,
    )