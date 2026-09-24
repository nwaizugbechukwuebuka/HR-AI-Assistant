from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    """Data required to create a conversation."""

    title: str = Field(
        default="New conversation",
        min_length=1,
        max_length=255,
    )


class ConversationResponse(BaseModel):
    """Conversation returned by the API."""

    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class MessageCreate(BaseModel):
    """User message submitted to the assistant."""

    content: str = Field(
        min_length=1,
        max_length=10000,
    )


class MessageResponse(BaseModel):
    """Message returned by the API."""

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ChatResponse(BaseModel):
    """Response returned after processing a chat message."""

    conversation_id: int
    user_message: MessageResponse
    assistant_message: MessageResponse