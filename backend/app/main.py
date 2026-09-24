from fastapi import FastAPI

from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.documents import router as documents_router
from backend.app.core.config import get_settings


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description="AI-powered HR knowledge and workflow assistant",
    version=settings.app_version,
)


app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/")
def root() -> dict:
    """Return basic application information."""

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }


@app.get("/health")
def health_check() -> dict:
    """Return application health status."""

    return {
        "status": "healthy",
    }