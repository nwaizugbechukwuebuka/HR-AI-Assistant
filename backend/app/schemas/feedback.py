from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    """Data submitted by a user about an AI response."""

    user_id: int
    message_id: str
    rating: str = Field(
        pattern="^(positive|negative)$",
    )
    comment: str | None = None


class FeedbackResponse(FeedbackCreate):
    """Persisted feedback representation."""

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )