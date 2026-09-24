from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def create_and_login_user() -> str:
    """Create a unique employee and return its JWT."""

    email = f"chat-{uuid4().hex}@example.com"
    password = "SecurePassword123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Chat Test User",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_conversation_requires_authentication() -> None:
    """Verify conversation creation requires authentication."""

    response = client.post(
        "/chat/conversations",
        json={
            "title": "HR Questions",
        },
    )

    assert response.status_code == 401


def test_create_conversation() -> None:
    """Verify an authenticated user can create a conversation."""

    token = create_and_login_user()

    response = client.post(
        "/chat/conversations",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "HR Questions",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "HR Questions"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_send_message() -> None:
    """Verify a user can send a message."""

    token = create_and_login_user()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    conversation_response = client.post(
        "/chat/conversations",
        headers=headers,
        json={
            "title": "Leave Policy",
        },
    )

    assert conversation_response.status_code == 201

    conversation_id = conversation_response.json()["id"]

    response = client.post(
        f"/chat/conversations/{conversation_id}/messages",
        headers=headers,
        json={
            "content": "How many vacation days do I have?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] == conversation_id
    assert data["user_message"]["role"] == "user"
    assert data["user_message"]["content"] == (
        "How many vacation days do I have?"
    )
    assert data["assistant_message"]["role"] == "assistant"


def test_user_cannot_access_another_users_conversation() -> None:
    """Verify conversation ownership is enforced."""

    first_token = create_and_login_user()

    first_conversation_response = client.post(
        "/chat/conversations",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
        json={
            "title": "Private Conversation",
        },
    )

    assert first_conversation_response.status_code == 201

    conversation_id = first_conversation_response.json()["id"]

    second_token = create_and_login_user()

    response = client.post(
        f"/chat/conversations/{conversation_id}/messages",
        headers={
            "Authorization": f"Bearer {second_token}",
        },
        json={
            "content": "Can I access this conversation?",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found."