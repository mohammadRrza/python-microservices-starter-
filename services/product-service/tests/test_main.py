from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "product-service"}


def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert data[0]["name"] == "Laptop"


def test_get_product_found():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 200
    assert response.json() == {"message": "Product not found"}