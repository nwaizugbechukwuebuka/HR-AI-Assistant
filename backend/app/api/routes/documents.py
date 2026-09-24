from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, require_role
from backend.app.db.database import get_db
from backend.app.db.models import User
from backend.app.schemas.document import DocumentCreate, DocumentResponse
from backend.app.services.document_service import register_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    document_data: DocumentCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(require_role("hr_admin")),
    ],
) -> DocumentResponse:
    """Register an HR knowledge document.

    Only HR administrators can register documents.
    """

    return register_document(
        db=db,
        document_data=document_data,
    )