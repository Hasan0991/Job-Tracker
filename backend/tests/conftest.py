import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import User, Job, Company, Application
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
    
    # Создаем тестовые записи
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
        first_name="User",
        last_name="Test"
    )
    same_job = Job(
        user_id=1,
        title="Backend Engineer",
        url="something.com"
    )
    additional_job = Job(
        user_id=2,
        title="Backend Engineer",
        url="something.com"
    )
    company = Company(
        user_id=1,
        name="Stark Industries",
        description="software",
        website="stark.com"
    )
    application = Application(
        user_id=1,
        job_id=1,
        cover_letter="something for now"
    )

    db.add_all([admin_user, user, same_job, additional_job, company, application])
    db.commit()

    # Обновляем объекты из базы
    db.refresh(admin_user)
    db.refresh(user)
    db.refresh(same_job)
    db.refresh(additional_job)
    db.refresh(company)
    db.refresh(application)

    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

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
