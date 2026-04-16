from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "gateway-service"}


@patch("app.main.httpx.get")
def test_get_users(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Ali", "email": "ali@example.com"}
    ]
    mock_get.return_value = mock_response

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json()[0]["email"] == "ali@example.com"
    mock_get.assert_called_once()


@patch("app.main.httpx.get")
def test_get_user(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ali",
        "email": "ali@example.com"
    }
    mock_get.return_value = mock_response

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@patch("app.main.httpx.post")
def test_create_user(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ali",
        "email": "ali@example.com"
    }
    mock_post.return_value = mock_response

    payload = {
        "name": "Ali",
        "email": "ali@example.com"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Ali"
    mock_post.assert_called_once()


@patch("app.main.httpx.get")
def test_get_products(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Laptop", "price": 1200}
    ]
    mock_get.return_value = mock_response

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Laptop"


@patch("app.main.httpx.get")
def test_get_orders(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "user_id": 1, "product_id": 2, "quantity": 3}
    ]
    mock_get.return_value = mock_response

    response = client.get("/orders")

    assert response.status_code == 200
    assert response.json()[0]["quantity"] == 3