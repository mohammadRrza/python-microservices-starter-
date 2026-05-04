from app.application.dto import AuthorizePaymentCommand, AuthorizePaymentResult
from app.domain.entities import Payment
from app.domain.events import PaymentAuthorized, PaymentFailed


class AuthorizePaymentUseCase:
    def __init__(self, payment_repository, payment_gateway, event_publisher):
        self.payment_repository = payment_repository
        self.payment_gateway = payment_gateway
        self.event_publisher = event_publisher

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
        self.event_publisher.publish(topic, event)

        return AuthorizePaymentResult(
            payment_id=payment.id,
            order_id=payment.order_id,
            status=payment.status.value,
        )