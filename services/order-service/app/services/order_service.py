import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.repositories.order_repository import OrderRepository
from app.schemas import OrderCreate


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def list_orders(self):
        return self.repository.list_all()

    def get_order(self, order_id: int):
        order = self.repository.get_by_id(order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    async def create_order(self, order_data: OrderCreate):
        async with httpx.AsyncClient(timeout=5.0) as client:
            user_response = await client.get(
                f"{settings.user_service_url}/internal/users/{order_data.user_id}"
            )

            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="User does not exist")

            product_response = await client.get(
                f"{settings.product_service_url}/products/{order_data.product_id}"
            )

            if product_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Product does not exist")

        product_data = product_response.json()
        price = product_data.get("price")

        if price is None:
            raise HTTPException(status_code=500, detail="Product price not found")

        total_price = float(price) * order_data.quantity

        return self.repository.create_with_outbox_event(
            user_id=order_data.user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_price=total_price,
        )