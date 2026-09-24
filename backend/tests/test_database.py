from sqlalchemy import text

from backend.app.db.database import SessionLocal, engine


def test_database_connection() -> None:
    """Verify that SQLAlchemy can connect to PostgreSQL."""

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_database_session() -> None:
    """Verify that a SQLAlchemy session can execute a query."""

    db = SessionLocal()

    try:
        result = db.execute(
            text("SELECT current_database()")
        )

        database_name = result.scalar()

        assert database_name == "hr_ai_assistant"

    finally:
        db.close()