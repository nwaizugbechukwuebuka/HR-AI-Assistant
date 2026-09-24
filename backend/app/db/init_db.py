from backend.app.db.database import Base, engine

# Import models so SQLAlchemy registers the tables.
from backend.app.db import models  # noqa: F401


def initialize_database() -> None:
    """Create database tables that do not already exist."""

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()
    print("Database tables initialized successfully.")