import os

os.environ["DATABASE_URL"] = "sqlite:///./tests/test.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "user-service"}


def test_create_user():
    payload = {
        "name": "Ali",
        "email": "ali@example.com"
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Ali"
    assert data["email"] == "ali@example.com"
    assert "id" in data


def test_create_user_duplicate_email():
    payload = {
        "name": "Ali",
        "email": "ali@example.com"
    }

    client.post("/users", json=payload)
    response = client.post("/users", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_get_users():
    client.post("/users", json={"name": "Ali", "email": "ali@example.com"})
    client.post("/users", json={"name": "Sara", "email": "sara@example.com"})

    response = client.get("/users")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Ali"
    assert data[1]["name"] == "Sara"


def test_get_user_found():
    create_response = client.post(
        "/users",
        json={"name": "Ali", "email": "ali@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "ali@example.com"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"