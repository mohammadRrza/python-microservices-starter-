from fastapi import Depends

from app.application.use_cases.authorize_payment import AuthorizePaymentUseCase
from app.infrastructure.db.repositories import SQLAlchemyPaymentRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.messaging.kafka_publisher import KafkaEventPublisher
from app.infrastructure.providers.mock_payment_gateway import MockPaymentGateway


def get_payment_repository(db=Depends(get_db)):
    return SQLAlchemyPaymentRepository(db)


def get_payment_gateway():
    return MockPaymentGateway()


def get_event_publisher():
    return KafkaEventPublisher()


def get_authorize_payment_use_case(
    repository=Depends(get_payment_repository),
    gateway=Depends(get_payment_gateway),
    publisher=Depends(get_event_publisher),
):
    return AuthorizePaymentUseCase(
        payment_repository=repository,
        payment_gateway=gateway,
        event_publisher=publisher,
    )