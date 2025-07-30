import pytest
from fastapi.testclient import TestClient
from app.main import app  
from sqlalchemy import create_engine
from app.database import get_db,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models import User
from app import utils
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    admin_user = User(
        email="admin@example.com",
        password=utils.hash_password("adminpass"),
        role="admin",
        first_name="Admin",
        last_name="User"
    )
    user = User(
        email="testuser1@example.com",
        password=utils.hash_password("testpassword1"),
        role="user",
        first_name="Admin",
        last_name="User"
    )
    db.add(user)  
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.refresh(user)
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


    
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

@pytest.fixture(scope="function")
def user_token_headers(client, db):
    login_data = {
        "username": "testuser1@example.com",
        "password": "testpassword1"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
