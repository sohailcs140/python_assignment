import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi import status
from app.db.database import Base, get_db
from app.main import app

DB_URL = "sqlite:///./test.db"
engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    db_session = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


def create_test_user():

    payload = {"email": "admin@gmail.com", "password": "admin"}

    response = client.post("/users/register/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED


def authenticate():
    create_test_user()
    payload = {"email": "admin@gmail.com", "password": "admin"}

    response = client.post("/users/login", json=payload)
    token = response.json().get("access_token")
    return token
