from app.domain.entities import Payment, PaymentStatus
from app.domain.repositories import PaymentRepository
from app.infrastructure.db.models import PaymentModel


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