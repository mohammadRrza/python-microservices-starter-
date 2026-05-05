from app.application.dto import AuthorizePaymentCommand, AuthorizePaymentResult
from app.domain.entities import Payment
from app.domain.events import PaymentAuthorized, PaymentFailed

class AuthorizePaymentUseCase:
    def __init__(self, payment_repository, payment_gateway, outbox_repository, db):
        self.payment_repository = payment_repository
        self.payment_gateway = payment_gateway
        self.outbox_repository = outbox_repository
        self.db = db

    def execute(self, command: AuthorizePaymentCommand) -> AuthorizePaymentResult:
        payment = Payment(
            order_id=command.order_id,
            amount=command.amount,
            currency=command.currency,
        )

        is_authorized = self.payment_gateway.authorize(
            amount=payment.amount,
            currency=payment.currency,
        )

        if is_authorized:
            payment.authorize()
            event = PaymentAuthorized(
                payment_id=payment.id,
                order_id=payment.order_id,
            )
            topic = "payment.authorized"
        else:
            payment.fail()
            event = PaymentFailed(
                payment_id=payment.id,
                order_id=payment.order_id,
            )
            topic = "payment.failed"

        self.payment_repository.save(payment)
        self.outbox_repository.save(
            aggregate_type="Payment",
            aggregate_id=str(payment.id),
            event_type=event.__class__.__name__,
            topic=topic,
            payload={
                "payment_id": str(payment.id),
                "order_id": str(payment.order_id),
                "status": payment.status.value,
                "amount": float(payment.amount),
                "currency": payment.currency,
            },
        )

        self.db.commit()
        print("OUTBOX SAVE CALLED")
        return AuthorizePaymentResult(
            payment_id=payment.id,
            order_id=payment.order_id,
            status=payment.status.value,
        )