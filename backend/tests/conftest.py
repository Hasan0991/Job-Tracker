import pytest
from fastapi.testclient import TestClient
from app.main import app  

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
@pytest.fixture
def admin_token_headers(client):
    
    login_data = {
        "username": "admin@example.com",
        "password": "adminpass"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}