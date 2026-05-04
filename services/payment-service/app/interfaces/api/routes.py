from fastapi import APIRouter, Depends

from app.application.dto import AuthorizePaymentCommand
from app.application.use_cases.authorize_payment import (
    AuthorizePaymentUseCase,
)
from app.infrastructure.db.repositories import (
    SQLAlchemyPaymentRepository,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.messaging.kafka_publisher import (
    KafkaEventPublisher,
)
from app.infrastructure.providers.mock_payment_gateway import (
    MockPaymentGateway,
)
from app.interfaces.api.schemas import (
    AuthorizePaymentRequest,
    PaymentResponse,
)

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post(
    "/authorize",
    response_model=PaymentResponse,
)
def authorize_payment(
    payload: AuthorizePaymentRequest,
    db=Depends(get_db),
):
    repository = SQLAlchemyPaymentRepository(db)

    gateway = MockPaymentGateway()

    publisher = KafkaEventPublisher()

    use_case = AuthorizePaymentUseCase(
        payment_repository=repository,
        payment_gateway=gateway,
        event_publisher=publisher,
    )

    result = use_case.execute(
        AuthorizePaymentCommand(
            order_id=payload.order_id,
            amount=payload.amount,
            currency=payload.currency,
        )
    )

    return PaymentResponse(
        payment_id=result.payment_id,
        order_id=result.order_id,
        status=result.status,
    )