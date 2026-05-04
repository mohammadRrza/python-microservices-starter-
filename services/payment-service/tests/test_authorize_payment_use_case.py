from app.application.dto import AuthorizePaymentCommand
from app.application.use_cases.authorize_payment import (
    AuthorizePaymentUseCase,
)


class FakeRepository:
    def __init__(self):
        self.saved_payment = None

    def save(self, payment):
        self.saved_payment = payment


class FakeGateway:
    def authorize(self, amount, currency):
        return True


class FakePublisher:
    def __init__(self):
        self.published_topic = None
        self.published_event = None

    def publish(self, topic, event):
        self.published_topic = topic
        self.published_event = event


def test_authorize_payment_use_case():
    repository = FakeRepository()

    gateway = FakeGateway()

    publisher = FakePublisher()

    use_case = AuthorizePaymentUseCase(
        payment_repository=repository,
        payment_gateway=gateway,
        event_publisher=publisher,
    )

    command = AuthorizePaymentCommand(
        order_id="order-123",
        amount=100,
        currency="USD",
    )

    result = use_case.execute(command)

    assert result.status == "authorized"

    assert repository.saved_payment is not None

    assert publisher.published_topic == "payment.authorized"

    assert publisher.published_event.order_id == "order-123"