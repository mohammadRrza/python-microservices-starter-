from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Product

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    db.add_all(
        [
            Product(name="Laptop", price=1200.0, description="Workstation laptop"),
            Product(name="Mouse", price=25.0, description="Wireless mouse"),
        ]
    )
    db.commit()
    db.close()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "product-service"}


def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Laptop"


def test_get_product_found():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Laptop"


def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product():
    response = client.post(
        "/products",
        json={"name": "Keyboard", "price": 75.5, "description": "Mechanical keyboard"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["name"] == "Keyboard"
    assert data["price"] == 75.5
    assert data["description"] == "Mechanical keyboard"