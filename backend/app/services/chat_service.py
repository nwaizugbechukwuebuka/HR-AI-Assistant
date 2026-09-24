from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import Conversation, Message


def create_conversation(
    db: Session,
    user_id: int,
    title: str = "New conversation",
) -> Conversation:
    """Create a conversation belonging to a user."""

    conversation = Conversation(
        user_id=user_id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_user_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> Conversation | None:
    """Retrieve a conversation belonging to a specific user."""

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )

    return db.scalar(statement)


def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    """Create a message inside a conversation."""

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: int,
) -> list[Message]:
    """Return messages belonging to a conversation."""

    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    return list(db.scalars(statement).all())