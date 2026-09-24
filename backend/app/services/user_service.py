from sqlalchemy.orm import Session

from backend.app.core.security import hash_password
from backend.app.db.models import User
from backend.app.db.repositories import get_user_by_email
from backend.app.schemas.user import UserCreate


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """Create a new application user."""

    existing_user = get_user_by_email(
        db=db,
        email=user_data.email,
    )

    if existing_user is not None:
        raise ValueError("A user with this email already exists.")

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role="employee",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user using email and password."""

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        return None

    from backend.app.core.security import verify_password

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    if not user.is_active:
        return None

    return user