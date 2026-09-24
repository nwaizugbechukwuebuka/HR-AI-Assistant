from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def create_test_user() -> tuple[str, str]:
    """Create a unique test user and return email and password."""

    email = f"test-{uuid4().hex}@example.com"
    password = "SecurePassword123"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Test Employee",
            "password": password,
        },
    )

    assert response.status_code == 201

    return email, password


def test_register_user() -> None:
    """Verify that a new user can register."""

    email = f"register-{uuid4().hex}@example.com"
    password = "SecurePassword123"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Registration Test User",
            "password": password,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["full_name"] == "Registration Test User"
    assert data["role"] == "employee"
    assert data["is_active"] is True

    assert "hashed_password" not in data
    assert "password" not in data


def test_duplicate_registration_is_rejected() -> None:
    """Verify that duplicate email registration is rejected."""

    email, password = create_test_user()

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Duplicate User",
            "password": password,
        },
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_login_returns_access_token() -> None:
    """Verify that valid credentials return a JWT."""

    email, password = create_test_user()

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_login_rejects_invalid_password() -> None:
    """Verify that an incorrect password is rejected."""

    email, _ = create_test_user()

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_me_requires_authentication() -> None:
    """Verify that /auth/me requires a valid JWT."""

    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_returns_authenticated_user() -> None:
    """Verify that /auth/me returns the authenticated user."""

    email, password = create_test_user()

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert data["role"] == "employee"
    assert data["is_active"] is True