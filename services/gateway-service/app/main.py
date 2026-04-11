import os
import httpx
from fastapi import FastAPI

app = FastAPI(title="Gateway Service")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8003")

@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway-service"}

@app.get("/users")
def users():
    response = httpx.get(f"{USER_SERVICE_URL}/users")
    return response.json()

@app.get("/products")
def products():
    response = httpx.get(f"{PRODUCT_SERVICE_URL}/products")
    return response.json()

@app.get("/orders")
def orders():
    response = httpx.get(f"{ORDER_SERVICE_URL}/orders")
    return response.json()