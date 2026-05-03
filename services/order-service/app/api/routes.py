from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas import OrderCreate, OrderResponse
from app.security import get_current_user
from app.services.order_service import OrderService

router = APIRouter()


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db))


@router.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@router.get("/orders", response_model=list[OrderResponse])
def get_orders(
    service: OrderService = Depends(get_order_service),
    current_user=Depends(get_current_user),
):
    return service.list_orders()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int = Path(..., gt=0),
    service: OrderService = Depends(get_order_service),
    current_user=Depends(get_current_user),
):
    return service.get_order(order_id)


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order: OrderCreate,
    service: OrderService = Depends(get_order_service),
    current_user=Depends(get_current_user),
):
    return await service.create_order(order)