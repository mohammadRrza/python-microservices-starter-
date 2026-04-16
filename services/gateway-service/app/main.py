import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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


# -----------------------------
# USERS
# -----------------------------

@app.get("/users/health")
async def users_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/health")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/users")
async def create_user(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}/users", json=payload)
    return JSONResponse(status_code=response.status_code, content=response.json())


# -----------------------------
# PRODUCTS
# -----------------------------

@app.get("/products/health")
async def products_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/health")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/products")
async def get_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/products")
async def create_product(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PRODUCT_SERVICE_URL}/products", json=payload)
    return JSONResponse(status_code=response.status_code, content=response.json())


# -----------------------------
# ORDERS
# -----------------------------

@app.get("/orders/health")
async def orders_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/health")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/orders")
async def get_orders():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/orders")
async def create_order(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ORDER_SERVICE_URL}/orders", json=payload)
    return JSONResponse(status_code=response.status_code, content=response.json())