import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.models import library  # imports the module


@pytest.mark.asyncio
async def test_signup_user(monkeypatch):
    # Mock async get_user_by_email
    async def mock_get_user_by_email(self, email: str):
        return None

    # Mock async add_user
    async def mock_add_user(self, user):
        return type("User", (), {
            "id": "fake_id_123",
            "name": user.name,
            "email": user.email,
            "role": "user"
        })()

    # Apply monkeypatch
    monkeypatch.setattr(library.LibraryDB, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(library.LibraryDB, "add_user", mock_add_user)

    # Test client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/signup", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        })

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
