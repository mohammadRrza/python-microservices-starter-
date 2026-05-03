import httpx
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from messaging.producer import start_kafka_producer, stop_kafka_producer, publish_event
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import verify_token
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import Order, OutboxEvent
from datetime import datetime, timezone
import asyncio
from app.schemas import OrderCreate, OrderResponse
from app.outbox_publisher import publish_outbox_events
from app.core.config import settings

security = HTTPBearer()

router = APIRouter()

USER_SERVICE_URL = settings.user_service_url
PRODUCT_SERVICE_URL = settings.product_service_url

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


@router.on_event("startup")
async def startup():
    await start_kafka_producer()
    asyncio.create_task(publish_outbox_events())
    print("Outbox publisher started")

@router.on_event("shutdown")
async def shutdown():
    await stop_kafka_producer()


@router.get("/")
def root():
    return {"message": "Order service is running"}


@router.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    async with httpx.AsyncClient(timeout=5.0) as client:
        user_response = await client.get(f"{USER_SERVICE_URL}/users/{order.user_id}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="User does not exist")

        product_response = await client.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
        )
        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product does not exist")

        product_data = product_response.json()
        price = product_data.get("price")

        if price is None:
            raise HTTPException(status_code=500, detail="Product price not found")

        total_price = float(price) * order.quantity

    db_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="pending",
    )

    db.add(db_order)
    db.flush()

    outbox_event = OutboxEvent(
        aggregate_type="Order",
        aggregate_id=db_order.id,
        event_type="OrderCreated",
        payload={
            "id": db_order.id,
            "user_id": db_order.user_id,
            "product_id": db_order.product_id,
            "quantity": db_order.quantity,
            "total_price": float(db_order.total_price),
        },
    )

    db.add(outbox_event)
    db.commit()
    db.refresh(db_order)

    return db_order