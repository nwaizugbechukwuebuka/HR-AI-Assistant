from sqlalchemy.orm import Session

from backend.app.db.models import Feedback
from backend.app.schemas.feedback import FeedbackCreate


def create_feedback(
    db: Session,
    feedback_data: FeedbackCreate,
) -> Feedback:
    """Store feedback for an AI-generated response."""

    feedback = Feedback(
        user_id=feedback_data.user_id,
        message_id=feedback_data.message_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback