from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "order-service"}


def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert data[0]["user_id"] == 1


def test_get_order_found():
     response = client.get("/orders/1")
     assert response.status_code == 200
     assert response.json()["id"] == 1


def test_get_order_not_found():
    response = client.get("/orders/999")
    assert response.status_code != 200
    assert response.json() == {"detail": "Order not found"}