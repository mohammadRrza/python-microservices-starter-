import os
import httpx
from fastapi import FastAPI, Request

app = FastAPI(title="Gateway Service")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8003")


@app.get("/")
def root():
    return {"message": "Gateway is running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway-service"}


@app.get("/users")
def get_users():
    response = httpx.get(f"{USER_SERVICE_URL}/users")
    return response.json()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    response = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}")
    return response.json()


@app.post("/users")
async def create_user(request: Request):
    payload = await request.json()
    response = httpx.post(f"{USER_SERVICE_URL}/users", json=payload)
    return response.json()


@app.get("/products")
def get_products():
    response = httpx.get(f"{PRODUCT_SERVICE_URL}/products")
    return response.json()


@app.get("/orders")
def get_orders():
    response = httpx.get(f"{ORDER_SERVICE_URL}/orders")
    return response.json()