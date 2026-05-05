from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_authorize_payment_api():
    response = client.post(
        "/payments/authorize",
        json={
            "order_id": "order-123",
            "amount": 100,
            "currency": "USD",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == "order-123"

    assert data["status"] == "authorized"

    assert "payment_id" in data