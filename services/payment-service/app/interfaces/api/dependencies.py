from fastapi import Depends
from sqlalchemy.orm import Session
from app.application.use_cases.authorize_payment import AuthorizePaymentUseCase
from app.infrastructure.db.repositories import SQLAlchemyPaymentRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.messaging.kafka_publisher import KafkaEventPublisher
from app.infrastructure.providers.mock_payment_gateway import MockPaymentGateway
from app.infrastructure.outbox.repository import SQLAlchemyOutboxRepository

def get_payment_repository(db=Depends(get_db)):
    return SQLAlchemyPaymentRepository(db)


def get_payment_gateway():
    return MockPaymentGateway()


def get_event_publisher():
    return KafkaEventPublisher()


def get_authorize_payment_use_case(
    db: Session = Depends(get_db),
):
    payment_repository = SQLAlchemyPaymentRepository(db)
    outbox_repository = SQLAlchemyOutboxRepository(db)
    payment_gateway = MockPaymentGateway()

    return AuthorizePaymentUseCase(
        payment_repository=payment_repository,
        payment_gateway=payment_gateway,
        outbox_repository=outbox_repository,
        db=db,
    )