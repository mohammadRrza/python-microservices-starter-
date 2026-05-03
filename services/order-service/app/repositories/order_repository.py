from sqlalchemy.orm import Session

from app.models import Order, OutboxEvent


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Order]:
        return self.db.query(Order).order_by(Order.id).all()

    def get_by_id(self, order_id: int) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def create_with_outbox_event(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
        total_price: float,
    ) -> Order:
        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status="pending",
        )

        self.db.add(order)
        self.db.flush()

        outbox_event = OutboxEvent(
            aggregate_type="Order",
            aggregate_id=order.id,
            event_type="OrderCreated",
            payload={
                "id": order.id,
                "user_id": order.user_id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "total_price": float(order.total_price),
            },
        )

        self.db.add(outbox_event)
        self.db.commit()
        self.db.refresh(order)

        return order