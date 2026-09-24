from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import Document, User


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """Retrieve a user by email address."""

    statement = select(User).where(User.email == email)

    return db.scalar(statement)


def create_document(
    db: Session,
    filename: str,
    title: str,
    file_path: str,
    document_type: str,
) -> Document:
    """Create and persist a document record."""

    document = Document(
        filename=filename,
        title=title,
        file_path=file_path,
        document_type=document_type,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document