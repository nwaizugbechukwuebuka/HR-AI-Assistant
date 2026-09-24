from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.db.database import get_db
from backend.app.db.models import User
from backend.app.schemas.chat import (
    ChatResponse,
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from backend.app.services.chat_service import (
    create_conversation,
    create_message,
    get_user_conversation,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_conversation(
    conversation_data: ConversationCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> ConversationResponse:
    """Create a conversation for the authenticated user."""

    return create_conversation(
        db=db,
        user_id=current_user.id,
        title=conversation_data.title,
    )


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=ChatResponse,
)
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> ChatResponse:
    """Store a user message and generate a temporary assistant response."""

    conversation = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    user_message = create_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=message_data.content,
    )

    assistant_message = create_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=(
            "The HR AI response service is not connected yet. "
            "Your message has been stored successfully."
        ),
    )

    return ChatResponse(
        conversation_id=conversation.id,
        user_message=user_message,
        assistant_message=assistant_message,
    )