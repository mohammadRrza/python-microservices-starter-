from app.domain.entities import Payment, PaymentStatus
from app.domain.repositories import PaymentRepository
from app.infrastructure.db.models import PaymentModel, OutboxEvent


class SQLAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, db):
        self.db = db

    def save(self, payment: Payment) -> None:
        model = PaymentModel(
            id=payment.id,
            order_id=payment.order_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status.value,
            created_at=payment.created_at,
        )

        self.db.add(model)
        self.db.commit()

    def get_by_id(self, payment_id: str) -> Payment | None:
        model = (
            self.db.query(PaymentModel)
            .filter(PaymentModel.id == payment_id)
            .first()
        )

        if model is None:
            return None

        payment = Payment(
            id=model.id,
            order_id=model.order_id,
            amount=model.amount,
            currency=model.currency,
        )

        payment.status = PaymentStatus(model.status)
        payment.created_at = model.created_at

        return payment
    
    def create_with_outbox_event(self, payment: Payment) -> Payment:
        payment_model = PaymentModel(
            id=payment.id,
            order_id=payment.order_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status,
        )

        self.db.add(payment_model)
        self.db.flush()

        outbox_event = OutboxEvent(
            aggregate_type="Payment",
            aggregate_id=str(payment_model.id),
            event_type="PaymentCreated",
            payload={
                "id": str(payment_model.id),
                "order_id": str(payment_model.order_id),
                "amount": float(payment_model.amount),
                "currency": payment_model.currency,
                "status": payment_model.status,
            },
        )

        self.db.add(outbox_event)
        self.db.commit()
        self.db.refresh(payment_model)

        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            amount=float(payment_model.amount),
            currency=payment_model.currency,
            status=payment_model.status,
        )