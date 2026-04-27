import datetime
import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from messaging.producer import start_kafka_producer, stop_kafka_producer, publish_event
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import verify_token
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db

security = HTTPBearer()

app = FastAPI(title="Order Service")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderResponse(OrderCreate):
    id: int


fake_orders = [
    {"id": 1, "user_id": 1, "product_id": 2, "quantity": 3},
    {"id": 2, "user_id": 2, "product_id": 1, "quantity": 1},
]

@app.on_event("startup")
async def startup():
    await start_kafka_producer()


@app.on_event("shutdown")
async def shutdown():
    await stop_kafka_producer()


@app.get("/")
def root():
    return {"message": "Order service is running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@app.get("/orders", response_model=List[OrderResponse])
def get_orders():
    return fake_orders


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    for order in fake_orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    ):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{USER_SERVICE_URL}/users/{order.user_id}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="User does not exist")

        product_response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{order.product_id}")
        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product does not exist")

    new_order = {
        "id": len(fake_orders) + 1,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
    }
    fake_orders.append(new_order)
    await publish_event(
        topic="orders.events",
        event={
            "event_type": "OrderCreated",
            "event_version": 1,
            "occurred_at": datetime.datetime.now().isoformat(),
            "data": new_order,
        },
    )
    return new_order