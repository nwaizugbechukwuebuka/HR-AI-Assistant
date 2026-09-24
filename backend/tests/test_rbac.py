from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.core.security import hash_password
from backend.app.db.database import SessionLocal
from backend.app.db.models import User
from backend.app.main import app


client = TestClient(app)


def create_user(
    role: str = "employee",
) -> tuple[str, str]:
    """Create a test user with the requested role."""

    email = f"{role}-{uuid4().hex}@example.com"
    password = "SecurePassword123"

    db = SessionLocal()

    try:
        user = User(
            email=email,
            full_name=f"Test {role.title()}",
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
        )

        db.add(user)
        db.commit()

    finally:
        db.close()

    return email, password


def login(
    email: str,
    password: str,
) -> str:
    """Authenticate a user and return the access token."""

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_employee_cannot_create_document() -> None:
    """Verify that employees cannot register HR documents."""

    email, password = create_user("employee")

    token = login(email, password)

    response = client.post(
        "/documents",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "filename": "employee_handbook.pdf",
            "title": "Employee Handbook",
            "file_path": "data/documents/employee_handbook.pdf",
            "document_type": "policy",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions."


def test_hr_admin_can_create_document() -> None:
    """Verify that HR administrators can register documents."""

    email, password = create_user("hr_admin")

    token = login(email, password)

    response = client.post(
        "/documents",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "filename": "leave_policy.pdf",
            "title": "Leave Policy",
            "file_path": "data/documents/leave_policy.pdf",
            "document_type": "policy",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["filename"] == "leave_policy.pdf"
    assert data["title"] == "Leave Policy"
    assert data["document_type"] == "policy"
    assert data["status"] == "pending"


def test_document_endpoint_requires_authentication() -> None:
    """Verify that document registration requires authentication."""

    response = client.post(
        "/documents",
        json={
            "filename": "test.pdf",
            "title": "Test Document",
            "file_path": "data/documents/test.pdf",
            "document_type": "policy",
        },
    )

    assert response.status_code == 401